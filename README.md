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

If the script finishes without errors, it should save the profiles in the `profiles` folder. Now please update the `config.ini` file to reflect your collection. Then try to run profiler against your own `cdx` file(s). This will generate profiles for your collection and will save them in the `profiles` directory (it will overwrite existing files with the same name).

```
$ python ./main.py path/to/cdx/files/*.cdx
```
