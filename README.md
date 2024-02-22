# Chum Web
Static website generator to generate a website for [SailfishOS:Chum](https://github.com/sailfishos-chum/), a Sailfish OS community repository.

For an overview of how this project is structured, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Running
In general, run it as `python -m chumweb`.  It will output the generated website to `out/www/`,
unless another directory has been specified by the option `out`.

Options can be specified on the command line in the form of `--option-name value` or
as an environment variable in the form of `CHUM_OPTION_NAME=value`.

The full list of options can be found in [chumweb/config.py](chumweb/config.py).

### Required options
* Either set:
  * `obs_user` and `obs_pass` to an user/password combo valid for the SailfishOS-OBS (which this tool uses by default).
    * Example: `CHUM_OBS_USER=johndoe` and `CHUM_OBS_PASS=hunter2`
  * `repos` to a list of repos.  (Handy when testing to avoid hitting OBS each time while developing.)
    * Example: `--repos 4.5.0.24_aarch64,4.5.0.24_i486`

### Other notable options
* `out=<path>`: change the output directory. Default: `out/`
* `debug=<bool>`: Enable debug output on the websites, such as package metadata on package sites.  Default: `false`
* `public_url=<str>`: The URL the generated website should be publicly available on.  Used to generate canonical URLs etc.
* `download_extra_metadata=<bool>`: Whether to download extra metadata from external sites, referenced by OBS metadata.  Default: `false`
  * This will cause site generation to take longer, so for some development tasks keep this set to `false`. ☺
* `repo_data_dir=<path>`: Directory with `{arch}-primary.xml.gz` files downloaded from an earlier run. 
  * You can set this to the value of `out/` to avoid downloading the repo each run while developing.

