from . import ci

from demorepo import config


def diff(args):

    paths = config.get_projects_paths()

    sha = args.get("sha")

    targets = ci.get_diff(paths, sha)

    print(" ".join(targets))
