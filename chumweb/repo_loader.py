"""
This module is responsible for finding package repos, downloading the indexes and parsing metadata.
"""
from functools import reduce
from gzip import GzipFile
from os import makedirs
from pathlib import Path
from typing import List, TypedDict, NotRequired, Unpack, Tuple, Dict
from urllib.parse import urljoin

from . import CONFIG
from .package import Package

import requests
import xml.dom.minidom as minidom

from .progress import begin_step, step_progress, StepHandle

DEFAULT_HEADERS = {
    "User-Agent": f"{CONFIG.user_agent} ({CONFIG.public_url}/about-generator.html)"
}

OBS_API_HEADERS = DEFAULT_HEADERS | {
    "Accept": "application/xml;charset=utf-8"
}


# OBS API: https://api.opensuse.org/apidocs/index#/Search/get_search_package
def list_obs_project_repos(obs_url: str, project: str, auth):
    """
    Lists the available repos on an Open Build Service Instance in a specified project, using the given
    authentication.
    """
    r = requests.get(urljoin(obs_url, f"build/{project}"), headers=OBS_API_HEADERS, auth=auth)
    doc = minidom.parseString(r.content)
    repos = [el.getAttribute("name") for el in doc.getElementsByTagName("entry")]
    return repos


def filter_newest_repos(repos: List[str]):
    """
    Return the list of repos with the newest version numbers

    Example:
        `get_newest_repos(["4.5.0.24_i486", "4.5.0.24_aarch64", "4.4.0.72_i486", "4.4.0.72_aarch64"])` returns
        `["4.5.0.24_i486", "4.5.0.24_aarch64"]`
    """

    def cmp_repo_version(left: str, right: str) -> str:
        """
        Compares two repos names `left` and `right`, returns the one with the newest version
        or `left` if the versions are equal
        """

        def ver_nos(repo_name: str):
            ver = repo_name.split("_")[0]
            return [int(part) for part in ver.split(".")]

        ver_l = ver_nos(left)
        ver_r = ver_nos(right)

        for (l, r) in zip(ver_l, ver_r):
            if l > r:
                return left
            elif l < r:
                return right
            else:
                continue

        return left

    # Find the repo with the highest version number (ignore the architecture)
    newest_version = reduce(cmp_repo_version, repos).split("_")[0] + "_"
    return [repo for repo in repos if repo.startswith(newest_version)]


class LoadRepoOptions(TypedDict):
    data_path: NotRequired[Path]
    repos: List[str]


def load_repo(obs_url: str, obs_project: str, obs_auth: Tuple[str, str], repo_url: str,
              out_dir: Path, **kwargs: Unpack[LoadRepoOptions]) -> List[Package]:
    if "repos" in kwargs:
        repos = kwargs["repos"]
    else:
        begin_step("Listing repos")
        repos = filter_newest_repos(list_obs_project_repos(obs_url, obs_project, obs_auth))

    if "data_path" in kwargs:
        data_paths = [Path(kwargs["data_path"], f"{repo}.xml.gz") for repo in repos]
    else:
        begin_step("Downloading repos")
        data_paths = [save_repo_data(urljoin(repo_url, repo_name + "/"), repo_name, out_dir) for repo_name in repos]

    all_pkgs = {}

    parse_step = begin_step("Parsing repo index")
    repo_count = len(repos)
    i = 1
    for data_path, repo_name in zip(data_paths, repos):
        step_progress(parse_step, repo_name, i, repo_count)
        arch = repo_name.split("_")[1]
        all_pkgs[arch] = read_repo_data(urljoin(repo_url, repo_name), data_path)
        link_debug_packages(all_pkgs[arch])
        i += 1

    all_pkg_list: Dict[str, Package] = {}

    begin_step("Combining repos")
    for arch, pkg_list in all_pkgs.items():
        for pkg in pkg_list:
            if pkg.name in all_pkg_list:
                all_pkg_list[pkg.name].merge_arch(pkg)
            else:
                all_pkg_list[pkg.name] = pkg

    if CONFIG.download_extra_metadata:
        remote_desc_step = begin_step("Loading remote descriptions")
        load_remote_descriptions(all_pkg_list.values(), remote_desc_step)

    return list(all_pkg_list.values())


def save_repo_data(repo_url: str, repo_name: str, out_dir: Path):
    """
    Given a `repo_url`, find and download the `primary.xml.gz` file into `out_dir`
    """
    makedirs(out_dir, exist_ok=True)
    r = requests.get(urljoin(repo_url, "repodata/repomd.xml"), headers=DEFAULT_HEADERS)
    xml = minidom.parseString(r.content)

    data_elements = xml.getElementsByTagName("data")

    primary_url: str | None = None
    for dataElement in data_elements:
        if dataElement.getAttribute("type") == "primary":
            locations = dataElement.getElementsByTagName("location")
            if len(locations) > 0:
                primary_url = locations[0].getAttribute("href")
                break

    if not primary_url:
        return

    primary_url = urljoin(repo_url, primary_url)
    primary_gz_path = out_dir.joinpath(f"{repo_name}.xml.gz")

    with open(primary_gz_path, "wb") as primaryGzFile:
        r = requests.get(primary_url, headers=DEFAULT_HEADERS)

        for chunk in r.iter_content(8096):
            primaryGzFile.write(chunk)

    return primary_gz_path


def read_repo_data(repo_url, repo_info: Path) -> List[Package]:
    """
    Reads all package data from a `primary.xml.gz` file
    """
    pkgs = []
    with GzipFile(repo_info) as gz:
        xml = minidom.parse(gz)
        for xmlPkg in xml.getElementsByTagName("package"):
            pkgs.append(Package.from_node(xmlPkg))

    return pkgs


def link_debug_packages(pkgs: List[Package]) -> None:
    """
    Links "debug" packages to the corresponding package. This method modifies given `pkgs` in-place
    """

    list.sort(pkgs, key=lambda p: p.name)
    last_pkg = None

    for pkg in pkgs:
        if pkg.name.endswith("-debuginfo"):
            last_pkg.debuginfo_package = pkg
            pass
        elif pkg.name.endswith("-debugsource"):
            last_pkg.debugsource_package = pkg
        else:
            last_pkg = pkg


def load_remote_descriptions(pkgs: List[Package], step: StepHandle):
    """
    Loads remote descriptions of the given pkgs and modifies them in place
    with the description.
    """
    from markdown import markdown
    from markupsafe import Markup
    pkgs_with_markdown = [pkg for pkg in pkgs if pkg.markdown_url]
    total_pkgs_with_markdown = len(pkgs_with_markdown)
    i = 1
    for pkg in pkgs_with_markdown:
        step_progress(step, pkg.name, i, total_pkgs_with_markdown)
        r = requests.get(pkg.markdown_url, headers=DEFAULT_HEADERS, allow_redirects=True)
        if r.ok:
            pkg.description = Markup(markdown(r.text, output_format="html"))
        i += 1
