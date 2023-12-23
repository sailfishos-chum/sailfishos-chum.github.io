"""
This package contains methods for writing Atom feeds
"""
from datetime import datetime
from typing import List, Optional, Iterable
from xml.dom.minidom import Document, Element

from chumweb import CONFIG
from chumweb.package import Package

# Reuse the namespace that the primary.xml.gz file uses
REPO_NS = "http://linux.duke.edu/metadata/common"


def create_atom_feed(public_url: str, title: str, updated: datetime) -> Document:
    """
    Creates a basic Atom feed, with no entries

    https://validator.w3.org/feed/docs/atom.html

    :return: The created feed as an XML Document
    """
    doc = Document()
    feed = doc.createElementNS("http://www.w3.org/2005/Atom", "feed")
    feed.setAttribute("xmlns", "http://www.w3.org/2005/Atom")
    feed.setAttribute("xmlns:repo", "http://linux.duke.edu/metadata/common")
    doc.appendChild(feed)

    el_id = _create_simple_element(doc, "id", public_url)
    feed.appendChild(el_id)

    el_title = _create_simple_element(doc, "title", title)
    feed.appendChild(el_title)

    el_updated = _create_simple_element(doc, "updated", updated.isoformat())
    feed.appendChild(el_updated)

    el_icon = _create_simple_element(doc, "icon", CONFIG.public_url + "static/img/sailfishos-chum.png")
    feed.appendChild(el_icon)

    feed.appendChild(_create_link_el(doc, public_url, rel="self"))

    return doc


def create_package_atom_feed(pkgs: List[Package], public_url: str, title: str) -> Document:
    """
    Creates a Atom feed with packages
    :return: An XML Document representing the feed
    """
    doc = create_atom_feed(public_url, title, pkgs[0].updated)
    feed = doc.getElementsByTagName("feed")[0]

    for pkg in pkgs:
        feed.appendChild(_create_pkg_entry(doc, pkg))

    return doc


def _create_pkg_entry(doc: Document, pkg: Package) -> Element:
    """
    Create a single entry for a package in an Atom feed
    :param doc: The document where the elements should be created in
    :param pkg: The package to create the entry for
    :return: An element representing the package
    """
    entry = doc.createElement("entry")

    entry_id = _create_simple_element(doc, "id", CONFIG.public_url + pkg.web_url())
    entry.appendChild(entry_id)

    entry_updated = _create_simple_element(doc, "updated", pkg.updated.isoformat())
    entry.appendChild(entry_updated)

    entry_title = _create_simple_element(doc, "title", pkg.title)
    entry.appendChild(entry_title)

    entry_link = _create_link_el(doc, CONFIG.public_url + pkg.web_url())
    entry.appendChild(entry_link)

    entry_content_text = f"Package {pkg.name} was updated to version {pkg.version.to_short_str()}"
    entry_content = _create_simple_element(doc, "content", entry_content_text, type="text")
    entry.appendChild(entry_content)

    # Add author names
    author_names = []

    if pkg.packager_name:
        author_names += [pkg.packager_name]
    if pkg.developer_name:
        author_names += [pkg.developer_name]

    for name in author_names:
        entry_author = _create_simple_element(doc, "author")
        entry_author_name = _create_simple_element(doc, "name", name)
        entry_author.appendChild(entry_author_name)
        entry.appendChild(entry_author)

    # Add categories
    for category in pkg.categories:
        entry_category = _create_simple_element(doc, "category", term=category)
        entry.appendChild(entry_category)

    # Add download links for RPM files
    for arch in pkg.archs:
        download_size = pkg.download_size[arch]
        entry_rpm_link = _create_link_el(doc, pkg.get_download_url(arch), rel="enclosure",
                                         length=download_size,
                                         title=f"{pkg.name}-{pkg.version.to_full_str()}-{arch}.rpm",
                                         type="application/x-rpm")
        entry.appendChild(entry_rpm_link)

    # Add chum-related metadata
    for arch in pkg.archs:
        pkg_el = _create_simple_element(doc, "repo:package", ns=REPO_NS, type="rpm")

        entry_chum_name = _create_simple_element(doc, "repo:name", pkg.name, REPO_NS)
        pkg_el.appendChild(entry_chum_name)

        entry_chum_arch = _create_simple_element(doc, "repo:arch", arch, ns=REPO_NS)
        pkg_el.appendChild(entry_chum_arch)

        entry_chum_version = _create_simple_element(doc, "repo:version", ns=REPO_NS,
                                                    epoch=pkg.version.epoch, ver=pkg.version.ver, rel=pkg.version.rel)
        pkg_el.appendChild(entry_chum_version)

        entry_chum_summary = _create_simple_element(doc, "repo:summary", pkg.summary, ns=REPO_NS)
        pkg_el.appendChild(entry_chum_summary)

        entry_chum_description = _create_simple_element(doc, "repo:description", pkg.description, ns=REPO_NS)
        pkg_el.appendChild(entry_chum_description)

        entry_chum_url = _create_simple_element(doc, "repo:url", pkg.url, ns=REPO_NS)
        pkg_el.appendChild(entry_chum_url)

        entry.appendChild(pkg_el)

    return entry


def _create_simple_element(doc: Document, tag_name: str, content: Optional[str | Element | Iterable[Element]] = None,
                           ns: Optional[str] = None, **attrs) -> Element:
    """
    Creates a XML tag with the given tag name, children and attributes
    :param tag_name: The name of the tag
    :param content: The content of the tag
    :param attrs: The attributes to set on the tag
    :return: The created tag
    """
    if ns:
        el = doc.createElementNS(ns, tag_name)
    else:
        el = doc.createElement(tag_name)

    if content is None:
        # Okay, do nothing
        pass
    elif type(content) is str:
        el.appendChild(doc.createTextNode(content))
    elif type(content) is Element:
        el.appendChild(content)
    elif type(content) is Iterable[Element]:
        for child in content:
            el.appendChild(child)
    else:
        assert False, "Unsupported content type: " + str(type(content))

    for key, value in attrs.items():
        el.setAttribute(key, value)

    return el


def _create_link_el(doc: Document, href: str, **kwargs):
    kwargs["href"] = href
    return _create_simple_element(doc, "link", **kwargs)
