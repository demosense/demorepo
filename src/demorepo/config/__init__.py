import os
import sys
import yaml

from demorepo import logger

__all__ = ["get_config", "get_projects"]

_config = {}


def get_config():
    _lazy_load()
    return _config


def get_projects():
    return list(get_config()["projects"].keys())


def get_projects_dependencies():
    projects = get_config()["projects"]
    deps = {p: v["depends"] for p, v in projects.items()}
    return deps


def get_projects_paths():
    projects = get_config()["projects"]
    paths = {p: v["path"] for p, v in projects.items()}
    return paths


def _init_config():

    # Load global config file
    config_path = os.path.join(os.getcwd(), "config.yml")

    # apply the order to the targets list, just if config.yml exists in root path
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = yaml.load(f.read())

        # Get and check projects
        projects = config.get("projects", [])
        # Check Schema:
        for p in projects.keys():
            # Path is required
            if "path" not in projects[p]:
                raise Exception(
                    "Error: Invalid project {} in config.yml. Path is required.".format(p))

            # Defaults
            projects[p]["depends"] = projects[p].get("depends", [])

        # TODO: Check that projects are directories

        _config['projects'] = projects

    else:
        logger.error("Error: Unable to find config.yml. Is this a demorepo?")
        sys.exit(-1)


def _lazy_load():
    if not _config:
        _init_config()
