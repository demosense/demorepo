import os
import git
import requests


__all__ = ['defaults', 'get_target_projects']


defaults = {
    "CI_SERVER_URL": "https://gitlab.com"
}


def info():
    return "Apart of env vars from pipeline, it requires GITLAB_API_KEY env var to use the gitlab api."


def get_target_projects(env_vars):
    git_branch = os.getenv("CI_COMMIT_REF_NAME")
    git_commit_tag = os.getenv("CI_COMMIT_TAG")
    if git_branch == "master" or git_commit_tag or "release" in git_branch:
        # Mark all the projects as targets
        targets = os.listdir(env_vars['PROJECTS_PATH'])
    else:
        # the actual python path is the root of a git project
        repo = git.Repo(os.getcwd())

        # get last green commit sha in this branch
        url = f"{env_vars['CI_SERVER_URL']}/api/v4/projects/{env_vars['CI_PROJECT_ID']}/pipelines"
        vars_get = f"?status=success&ref={env_vars['CI_COMMIT_REF_NAME']}&per_page=1"
        response = requests.get(url+'/'+vars_get, headers={"PRIVATE-TOKEN": env_vars['GITLAB_API_KEY']}).json()
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
            last_green_commit = repo.merge_base(parent_branch, env_vars['CI_COMMIT_SHA'])[0].hexsha

            print(f"Using as last green commit the last commit in common between parent branch {parent_branch} "
                  f"and HEAD: {last_green_commit}")
        else:
            last_green_commit = response[0]["sha"].strip()

        print(f"sha of last green commit in the branch {git_branch} is {last_green_commit}")

        # Get git differences between index and last green commit
        targets = repo.git.diff(last_green_commit, name_only=True).split('\n')

        s = set()
        nchars_projects_path = len(env_vars['PROJECTS_PATH'])+1 # Include the '/' to compare and to remove
        for t in targets:
            # Check that the modified path starts from the projects path
            if env_vars['PROJECTS_PATH']+'/' == t[:nchars_projects_path]:
                # Remove the first part (projects path)
                t = t[nchars_projects_path:]
                # Remove from the first / to the end
                if t.find('/') >= 0:
                    t = t[:t.find('/')]
                # Add it into a set (a way to get unique target names)
                s.add(t)
        targets = list(s)
        print(f"Unprocessed target folder names: {targets}")

    return targets
