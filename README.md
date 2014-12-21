# Archive Profiler

Scripts to generate profiles of various Web archives that will be saved in [Archive Profiles Repository](https://github.com/oduwsdl/archive_profiles).

## Running Profiler Script

To setup and run the Profiler script, please follow these steps:

Clone the repository.

```
$ git clone git@github.com:oduwsdl/archive_profiler.git
```

Change working directory.

```
$ cd archive_profiler
```

Install dependencies from the requirement file (add `sudo` before `pip` command if necessary.)

```
$ pip install -r requirements.txt
```

Run the script on the shipped sample `cdx` files.

```
$ python ./main.py cdx/*.cdx
```

If the script finishes without errors, it should save the profile in the `json` folder as well as push a copy to GitHub as a public Gist (respected path and URI will be shown on stdout). Now please update the `config.ini` file to reflect your collection. Then try to run profiler against your own (preferably small set of) `cdx` file(s). This operation will push the generated profile into a [public gist](https://gist.github.com/ibnesayeed). To disable posting profile to GitHub, set `write_to_github` to `no` in `config.ini` file and to change the Gist location, update the `github` section of `config.ini` with appropriate values.

```
$ python ./main.py path/to/cdx/files/*.cdx
```
