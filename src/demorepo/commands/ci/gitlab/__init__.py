import os
import git
import requests

from demorepo import logger


__all__ = ['defaults', 'get_lgc']


defaults = {
    "CI_SERVER_URL": "https://gitlab.com"
}


def info():
    return "Apart of env vars from pipeline, it requires GITLAB_API_KEY env var to use the gitlab api."


def get_lgc(env_vars):
    git_branch = os.getenv("CI_COMMIT_REF_NAME")

    # the actual python path is the root of a git project
    repo = git.Repo(os.getcwd())

    # get last green commit sha in this branch
    url = "{}/api/v4/projects/{}/pipelines".format(
        env_vars['CI_SERVER_URL'], env_vars['CI_PROJECT_ID'])
    vars_get = "?status=success&ref={}&per_page=1".format(
        env_vars['CI_COMMIT_REF_NAME'])
    response = requests.get(
        url+'/'+vars_get, headers={"PRIVATE-TOKEN": env_vars['GITLAB_API_KEY']}).json()
    if len(response) == 0:
        # No green pipelines on this branch. First commit in this pipeline branch or just sequence of red commits.
        # In any case, we first obtain the initial branch commit, represented as the last commit in the branch in
        # common with the parent. As we use git flow, the order is: master > release* develop > feature*

        # Get parent branch. If develop, master is the parent (from release, merge to master and develop)
        if git_branch == "develop":
            parent_branch = "origin/master"
        else:
            parent_branch = "origin/develop"

        # Commits in both this branch and in develop. Get the newer one.
        last_green_commit = repo.merge_base(
            parent_branch, env_vars['CI_COMMIT_SHA'])[0].hexsha

        logger.info("Using as last green commit the last commit in common between "
                    "parent branch {} and HEAD: {}".format(parent_branch, last_green_commit))
    else:
        last_green_commit = response[0]["sha"].strip()

    logger.info("sha of last green commit in the branch {} is {}".format(git_branch, last_green_commit))

    return last_green_commit
