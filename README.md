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

If it works please update the `config.ini` file to reflect your collection. Then try to run profiler against your own (preferably small set of) `cdx` file(s).

Warning: This operation will push the generated profile into a [public gist](https://gist.github.com/ibnesayeed). Please be sure about the privacy concerns you may have.

```
$ python ./main.py path/to/cdx/files/*.cdx
```
