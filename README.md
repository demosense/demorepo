# Demosense's demorepo

This project is a python3 package which can be installed from git using pip3.

## Installation

We recommend to install the package in a virtual environment. However, it can be installed as well in your system or user python installation. In any case, use `pip3`:

```
pip3 install git+https://github.com/demosense/demorepo.git
```

## Configuration

Demorepo requires a configuration file:

* `demorepo.yml`

This file configures the tracked projects, their dependencies, ci tools and predefined stages. The following YAML schema provides an example:

```yaml
demorepo: 1.0

projects:
    project-a-name:
        path: /path/to/project-a
    project-b-name:
        path: /path/to/project-b
        depends:
            - project-a-name
stages:
    stage-a:
        script: command
        projects:
            - project-a

    stage-b:
        script: command
        projects:
            - project-a
            - project-b
```

## Usage

Demorepo is a CLI tool. The help option (-h) will always print useful information for commands and subcommands. To run a command just run the demorepo module like this:

```
python3 -m demorepo [command] [options]
```

### Available Commands

* `run`: Runs a particular command for selected stages.
* `stage`: Used to run scripts related to stages in `demorepo.yml`.
* `diff`: Returns a list of targets that have changed for a particular commit SHA.
* `lgc`: Stands for _last green commit_, returns the last comment to report a completed integration step for the configured CI tool.

### run

```
demorepo run [-h] [-t TARGETS] [-e ENV] [--reverse-targets] [--stop-on-error] command
```

Execute a shell command for all projects.

```
positional arguments:
  command               The shell command to execute.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGETS, --targets TARGETS
                        A list of target project names to run the provided
                        stage, separated by blank spaces (use quotes around
                        the string).
  -e ENV, --env ENV     Optional variables passed to the target stage script.
                        The format is VAR_NAME=VAR_VALUE. Multiple env vars
                        can be specified.
  --reverse-targets     Reverse the dependency order for projects
  --stop-on-error       Stops the execution if the command fails for a project
```

### run-stage

```
demorepo stage [-h] [-e ENV] [-t TARGETS] [--reverse-targets] [--stop-on-error] stage
```

Run the specified stage in the global and local config files.

```
positional arguments:
  stage                 Stage name in the project demorepo.yml

optional arguments:
  -h, --help            show this help message and exit
  -e ENV, --env ENV     Optional variables passed to the target stage script.
                        The format is VAR_NAME=VAR_VALUE. Multiple env vars
                        can be specified.
  -t TARGETS, --targets TARGETS
                        A list of target project names to run the provided
                        stage, separated by blank spaces (use quotes around
                        the string).
  --reverse-targets     Reverse the dependency order for projects
  --stop-on-error       Stops the execution if the stage fails for a project
```

### diff

```
demorepo diff [-h] sha
```

Return the projects that have changed according to the provided sha

```
positional arguments:
  sha         SHA of the commit to compare with

optional arguments:
  -h, --help  show this help message and exit
```

### lgc

```
demorepo lgc [-h] [--ci-tool {gitlab}] [--ci-url CI_URL]
```

Return the last green commit according to the configured ci tool in the config

```
optional arguments:
  -h, --help          show this help message and exit
  --ci-tool {gitlab}  The specific CI tool (e.g.: gitlab, Circle-CI, ....)
  --ci-url CI_URL     the URL to the CI Server. By default uses the general
                      public URL.
```

# Contributing

## Dependencies

The `requirements.txt` file contains the python3 dependencies: `requests`, `GitPython` and `PyYAML`. The file `requirements_dev.txt` contains the extra dependencies for tests: `pytest` and `flake8`.

## Running unit tests

In the root folder run:

```
python3 setup.py test
```

_Note: Remember to install the requirements_dev.txt dependencies._
