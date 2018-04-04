import yaml
import os

from . import METADATA_PATH


def info(args):
    config_path = os.path.join(os.getcwd(), 'config.yml')
    # read config.yml
    if not os.path.exists(config_path):
        print("ERROR: File config.yml does not exists.")
        return

    with open(config_path) as f:
        config = yaml.load(f.read())

    if args['section'] == 'demorepo':
        _demorepo(config["demorepo"], args)
    elif args['section'] == 'ci-tool':
        _ci_tool(config["ci-tool"], args)
    elif args['section'] == 'projects':
        _projects(config["projects"], args)
    else:
        print(f"Section option '{args['section']}' not supported.")


def _demorepo(config, args):
    if args["version"]:
        print(config["version"])
    else:
        print("No valid option provided for info demorepo.")


def _ci_tool(config, args):
    if args["name"]:
        print(config["name"])
    elif args["url"]:
        print(config["url"])
    else:
        print("No valid option provided for info ci-tool.")


def _projects(config, args):
    if args["path"]:
        print(config["path"])
    else:
        print("No valid option provided for info projects.")
