from pathlib import Path

from chumweb import CONFIG
from chumweb.static_site_gen import gen_site
from chumweb.repo_loader import load_repo

repos = [f"4.5.0.24_{arch}" for arch in ["aarch64", "armv7hl", "i486"]]

out_dir: Path = Path(CONFIG.out_dir)

load_repo_kwargs = dict()
if CONFIG.repos:
    load_repo_kwargs["repos"] = CONFIG.repos
if CONFIG.repo_data_dir:
    load_repo_kwargs["data_path"] = Path(CONFIG.repo_data_dir)

pkgs = load_repo(CONFIG.obs_url, CONFIG.obs_project, (CONFIG.obs_user, CONFIG.obs_pass), CONFIG.repo_url_prefix,
                 out_dir, **load_repo_kwargs)
gen_site(pkgs, out_dir)
