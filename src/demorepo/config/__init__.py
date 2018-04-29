import os
import sys
import yaml

from demorepo import logger

__all__ = ["get_config", "get_projects", "get_projects_paths", "get_projects_dependencies", "get_stages"]

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


def get_stages():
    return get_config()["stages"]


def _init_config():

    # Load global config file
    config_path = os.path.join(os.getcwd(), "demorepo.yml")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = yaml.load(f.read())

        # PROJECTS:
        #
        projects = config.get("projects", {})
        # Check Schema:
        for p in projects.keys():
            # Path is required
            if "path" not in projects[p]:
                raise Exception(
                    "Error: Invalid project {} in config.yml. Path is required.".format(p))

            # Defaults
            projects[p]["depends"] = projects[p].get("depends", [])

        # TODO: Check that projects exists as directories

        _config['projects'] = projects

        # STAGES:
        #
        stages = config.get("stages", {})
        # Check Schema:
        for s in stages.keys():
            # Script is required
            if "script" not in stages[s]:
                raise Exception(
                    "Error: Invalid stage {} in config.yml. Script is required.".format(s))
            # Projects is required
            if "projects" not in stages[s]:
                raise Exception(
                    "Error: Invalid stage {} in config.yml. Projects is required.".format(s))

            included_project = stages[s]['projects']
            # Check if projects are defined
            for p in [p for p in included_project if p not in projects.keys()]:
                raise Exception(
                    "Error: Unrecognized project {} defined for stage {} in global demorepo.yml".format(p, s))

        _config['stages'] = stages

    else:
        logger.error("Error: Unable to find config.yml. Is this a demorepo?")
        sys.exit(-1)


def _lazy_load():
    if not _config:
        _init_config()
