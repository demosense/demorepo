# demorepo
---

This project is a python3 package which can be installed from git using pip3.

# Dependencies
---

The `requirements.txt` file contains the python3 dependencies: `requests`, `GitPython` and `PyYAML`. The file `requirements_dev.txt` contains the extra dependencies for tests: `pytest` and `flake8`.

# Installation
---

We recommend to install the package in a virtual environment. However, it can be installed as well in your system or user python installation. In any case, use `pip3`:

```
pip3 install git+https://github.com/demosense/demorepo.git
```

# Running unit tests
---

In the src folder (where the setup.cgf is placed) run:

```
python3 -m pytest -v .
```

_Note: Remember to install the requirements_dev.txt dependencies._

# Usage
---

It is used as a CLI tool. It has been implemented using [argparser](https://docs.python.org/3/library/argparse.html). The help option (-h) will always print useful information for commands and subcommands. To run a command just run the demorepo module like this:

```
python3 -m demorepo [command] [options]
```

## Commands

There are four commands which can be used:
-  init: Not implemented yet. Will be used to create the demorepo `config.yml` file, which will include the metadata about the demorepo.
-  info: Used to print the metadata stored in the `config.yml` file. Right now it is created manually, but will be handled by the demorepo tool.
-  run: Used to run scripts related to stages in `demorepo.yml` files placed in individual project folders.
-  integration: Not implemented yet. Will be used to run integration tests.

### init

Not implemented yet


### info

```
python3 -m demorepo init {section} {field}
```

Get the `field` (parameter flags, i.e.: `-v` to get the version) information stored in the section, where available sections are:

-  demorepo: Information about the demorepo. Available fields are:
    -  -v: The version of the demorepo.
-  ci-tool: 
    -  -n / --name: The ci-tool name.
    -  -u / --url: The url of the ci-tool.
-  projects: 
    -  -p / --path: The path to the projects folder, where projects are located in.
    -  -o / --order: Dependency order of the projects to run the stages. Not specified projects have no dependencies.

An example of config.yml:

```
demorepo:
    version: 1.0.0

ci-tool:
    name: gitlab
    url: https://gitlab.com
    
projects:
    path: projects
    order:
        - p3
        - p2
```

### run

```
python3 -m demorepo run {options}
```

Run the stage script (**right now only one script per stage is allowd**) for each target project. The target projects are selected by the option `-t` or `--all-targets`. Otherwise, the ci-tool will be used to get the last green commit and select the target projects those which have been modified from such commit.

Each project **must** include a `demorepo.yml` file (otherwise it is not considered a project by the CLI tool). The structure of this file is `stage: shell command` (_we recommend the shell command to be a path to an executable script_). An example of `demorepo.yml` file is as follows:

```
test:
    script: ./test.sh 

deploy: 
    script: ./deploy.sh $my_var1 $my_var2
```

The options of the run command are:

#### **Mandatory:**

-  -s / --stage [STAGE]: The stage to run the commands from `demorepo.yml`.
-  -p / --path [PATH]: The path to the projects folder.

#### **Optional:**

-  -r / --recursive: Detect inter-project dependencies and, if one project is selected as target, all the projects which depends on such project will be considered as targets too. **Only implemented for python projects.**
-  -t / --targets: A list of target project names, separated by commas. It is recommended to wrap it in double quotes (mandatory if there are blank spaces in the string)
-  --all-targets: If this flag is present, all the projects will be selected as targets.
-  --ci-tool: if -t and --all-targets are not used, the ci-tool will be used to select the target projects. This parameter is the name of the ci-tool to be used. **Right now it is only implemented for gitlab**. gitlab is the default value.
-  --ci-url: The url for the ci-tool to be used.

### integration

Not implemented yet
