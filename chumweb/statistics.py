from typing import Tuple, List, TextIO

from chumweb import CONFIG
from chumweb.repo_loader import RepoInfo


class MarkdownWriter:
    out: TextIO

    def __init__(self, out):
        self.out = out

    def write_mermaid_pie(self, title: str, data: List[Tuple[str, int]]) -> str:
        # Mermaid pie is the best kind of ie
        lines = [
                    "```mermaid",
                    "pie showData",
                    f"\ttitle {title}"
                ] + [f"\t\"{name}\": {count}" for name, count in data] + [
                    "```"
                ]
        self.out.write("\n".join(lines) + "\n")

    def write_header(self, title: str, level: int):
        self.out.write("#" * level + " " + title + "\n")

    def write_h1(self, title: str):
        self.write_header(title, 1)

    def write_h2(self, title: str):
        self.write_header(title, 2)

    def write_h3(self, title: str):
        self.write_header(title, 3)

    def write_p(self, text):
        self.out.write(text + "\n\n")

    def write_table(self, header: List[str], rows: List[List[str]]):
        self.out.write("| " + " | ".join(header) + " |\n")
        self.out.write("|" + "|".join(["---"] * len(header)) + "|\n")
        for row in rows:
            self.out.write("| " + " | ".join(row) + " |\n")

    def write_list(self, items: List[str]):
        for item in items:
            self.out.write("  * " + item + "\n")
        self.out.write("\n")


def write_job_summary(repo_info: RepoInfo):
    package_count = len(repo_info.packages)
    app_count = len([pkg for pkg in repo_info.packages if pkg.is_app()])

    pkgs_with_metadata_errs = [pkg for pkg in repo_info.packages if len(pkg.debug_yaml_errors)]
    pkgs_with_metadata_errs_count = len(pkgs_with_metadata_errs)

    apps_without_icon = [pkg for pkg in repo_info.packages if pkg.is_app() and pkg.icon is None]
    apps_without_icon_count = len(apps_without_icon)

    with open(CONFIG.job_summary, "w") as out:
        writer = MarkdownWriter(out)
        writer.write_h1("Output report")
        writer.write_p(f"Chum has run! Visit it at {CONFIG.public_url}")
        writer.write_h2("Package statistics")
        writer.write_mermaid_pie("Apps and packages", [
            ("Apps", app_count),
            ("Packages", package_count - app_count)
        ])
        writer.write_h2("Metadata errors")
        writer.write_mermaid_pie("Packages with metadata errors", [
            ("No error", package_count - pkgs_with_metadata_errs_count),
            ("Error", pkgs_with_metadata_errs_count)
        ])
        writer.write_p("List of packages with errors:")
        writer.write_table(["Package name", "Errors"],
                           [[pkg.name, ", ".join([str(err) for err in pkg.debug_yaml_errors])] for pkg in pkgs_with_metadata_errs])
        writer.write_p("Apps without icons are also a pretty good indicator that the YAML parsing broke, since most "
                       "apps have an icon and if they don't, usually the metadata parsing broke. Here is an overview "
                       "of apps without icon")
        writer.write_mermaid_pie("App icon overview", [
            ("Apps with icon", app_count - apps_without_icon_count),
            ("Apps without icon", apps_without_icon_count)
        ])
        writer.write_p("List of apps without icon:")
        writer.write_list([app.name for app in apps_without_icon])
