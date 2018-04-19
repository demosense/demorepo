import git
import importlib
import os

__all__ = ['get_lgc', 'get_diff']


def get_lgc(ci_tool, ci_url):

    # import ci module based on ci-tool parameter. Options: gitlab
    ci_module = importlib.import_module(
        name=".{}".format(ci_tool), package=__name__)

    # Clone the actual environ (contains required env vars) and append new ones for the child process
    child_environ = os.environ.copy()
    child_environ["CI_SERVER_URL"] = ci_url or ci_module.defaults["CI_SERVER_URL"]

    # get the target projects based on differences with respect to last green commit
    return ci_module.get_lgc(child_environ)


def get_diff(paths, sha):

    # the actual python path is the root of a git project
    repo = git.Repo(os.getcwd())

    # Get git differences between index and last green commit
    diffs = repo.git.diff(sha, name_only=True).split('\n')

    targets = []
    # Include the '/' to compare and to remove
    for p, path in paths.items():
        len_path = len(path)
        if any(path == d[:len_path] for d in diffs):
            targets.append(p)

    return targets
