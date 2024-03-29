# Chum Web Generator

Static website generator to generate a "**Chum Web**" website for [SailfishOS:Chum](https://github.com/sailfishos-chum/), a Sailfish&nbsp;OS community repository.

For an overview of how this project is structured, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Running

In general, run it as `python -m chumweb`.  It will output the generated website to a subdirectory `www/` of the
directory specified by the option `out`, i.e. `out/www/` by default (if the option `out` has not been explicitly set).

Options can be specified on the command line in the form of `--option-name value` or
as an environment variable in the form of `CHUM_OPTION_NAME=value`.

The full list of options can be found in [chumweb/config.py](chumweb/config.py).

### Required options

You must set one of the two following options:

* `obs_user` and `obs_pass` to an user/password combo valid for the SailfishOS-OBS (which this tool uses by default).
   
  Example: `CHUM_OBS_USER=johndoe` and `CHUM_OBS_PASS=hunter2`

* `repos` to a list of repos.  (Handy when testing to avoid hitting OBS each time while developing.)
  
  Example: `--repos 4.5.0.24_aarch64,4.5.0.24_i486`

### Other notable options

* `out=<path>`: change the output directory.

  Default value: `out/`

* `debug=<bool>`: Enable debug output on the websites, such as package metadata on package sites.

  Default value: `false`

* `public_url=<str>`: The URL the generated website should be publicly available on.  Used to generate canonical URLs etc.

* `download_extra_metadata=<bool>`: Whether to download extra metadata from external sites, referenced by OBS metadata.

  Default value: `true`<br />

  The default value causes site generation to take longer, so for some development tasks you may want to set this to `false`. ☺

* `repo_data_dir=<path>`: Directory with `{arch}-primary.xml.gz` files downloaded from an earlier run. 

  You can set this to the value of the option `out` (e.g. `out/`) to avoid downloading the repo each run while developing.

