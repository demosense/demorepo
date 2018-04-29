import yaml
import os

from . import METADATA_PATH
from demorepo import logger


def info(args):
    config_path = os.path.join(os.getcwd(), 'config.yml')
    # read config.yml
    if not os.path.exists(config_path):
        logger.info("ERROR: File config.yml does not exists.")
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
        logger.info("Section option '{}' not supported.".format(args['section']))


def _demorepo(config, args):
    if args["version"]:
        logger.info(config["version"])
    else:
        logger.info("No valid option provided for info demorepo.")


def _ci_tool(config, args):
    if args["name"]:
        logger.info(config["name"])
    elif args["url"]:
        logger.info(config["url"])
    else:
        logger.info("No valid option provided for info ci-tool.")


def _projects(config, args):
    if args["path"]:
        logger.info(config["path"])
    elif args["order"]:
        logger.info(config["order"])
    else:
        logger.info("No valid option provided for info projects.")
