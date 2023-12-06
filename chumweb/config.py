"""
Simple and hastily written configuration system that parses
environment variables/cli arguments parser
"""
import os
import sys
from dataclasses import dataclass, field, fields, Field
from typing import List


@dataclass
class Config:
    ###########################################################################
    # Required options                                                        #
    ###########################################################################

    # User for the open build system if no repos are specified. Needed for OBS api access
    obs_user: str | None = None
    # Password for the open build system
    obs_pass: str | None = None

    ###########################################################################
    # Optional options (with provided defaults)                               #
    ###########################################################################
    # Directory to store output
    out_dir: str = "out/"
    # A list of repos to download
    repos: List[str] = field(default_factory=list)
    # The open build service location
    obs_url: str = "https://build.sailfishos.org/"
    # The Open Build Service project that contains Chum
    obs_project: str = "sailfishos:chum"
    # The prefix of the repository where packages are published. The values from architecture-specific
    # repos will be appended
    repo_url_prefix: str = "https://repo.sailfishos.org/obs/sailfishos:/chum/"
    # Whether to show package parsing warnings and other debugging information
    debug: bool = False
    # Package names that are considered installers for Chum. These will not show the
    # "please install via chum" notice.
    chum_installer_pkgs: List[str] = field(default_factory=lambda: ["sailfishos-chum-gui-installer"])
    # Public, canonical URL
    public_url: str = "http://localhost:8000/"
    # Whether to download MarkDown descriptions et cetera. Turn off for faster local testing
    download_extra_metadata: bool = True
    # Directory with {arch}-primary.xml.gz files downloaded from an earlier run.
    repo_data_dir: str | None = None
    user_agent: str = "chumweb/1.0"
    source_code_url: str = ""
    featured_apps_count = 10
    updated_apps_count = 6
    # Where to output the Job summary (a Markdown file giving a summary of the job)
    job_summary = "out/summary.md"


def init_config() -> Config:
    """
    Loads config values from either command line arguments as `--config-value=x` or environment variables
    CHUM_CONFIG_VALUE=x
    """
    import getopt
    import sys

    c = Config()
    def env_name(key: str):
        return "CHUM_" + key.upper()

    def arg_name(key: str):
        return key.replace("_", "-")

    def set_option(f: Field, val: str):
        if f.type is bool:
            val = val.lower() == "true"
        if f.type is List[str]:
            val = val.split(",")
        setattr(c, f.name, val)

    cli_opts, cli_args = getopt.getopt(sys.argv[1:], "", [f"{arg_name(f.name)}=" for f in fields(Config)])

    for f in fields(Config):
        env_val = os.getenv(env_name(f.name))
        if env_val:
            set_option(f, env_val)

        for opt, arg in cli_opts:
            if opt.removeprefix("--") == arg_name(f.name):
                set_option(f, arg)

    return c


def validate_config(c: Config):
    def exit_with_error(err: str):
        sys.exit(err)
    if len(c.repos) == 0 and not c.obs_user:
        exit_with_error("Either a list of repos must be specified or an obs_user and obs_password must be given")


CONFIG = init_config()
