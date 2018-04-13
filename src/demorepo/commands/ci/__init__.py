import os
import importlib
from demorepo.commands.targets import filter_targets, append_dependencies


__all__ = ['get_targets']


def get_targets(args):
    # import ci module based on ci-tool parameter. Options: gitlab
    ci_module = importlib.import_module(
        name=f".{args['ci_tool']}", package=__name__)

    # Clone the actual environ (contains required env vars) and append new ones for the child process
    child_environ = os.environ.copy()
    child_environ["CI_SERVER_URL"] = args.get(
        'ci-url') or ci_module.defaults["CI_SERVER_URL"]
    child_environ["PROJECTS_PATH"] = args['path']

    # get the target projects based on differences with respect to last green commit
    targets = ci_module.get_target_projects(child_environ)

    # TARGET_SUBPROJECTS might contain residual folders or files. A project should be a folder with the
    # demorepo.yml file inside. Also, it might contain even deleted subprojects (are git differences!).
    # Remove them if they do not exist.
    targets = filter_targets(targets, args)
    # print(f"Filtered target projects are: {targets}")

    # If argument recursive_deps is True, we include in the targets the dependencies of the modified projects (targets)
    # NOTE: Actually this is only implemented for Python projects, based on requirements file dependencies.
    # Python dependencies process:
    # This is a recursive process which checks any requirements.* file inside each project.

    if args['recursive_deps']:
        targets = append_dependencies(targets, args)
        # print(f"Target projects with dependencies are: {targets}")

    # if len(targets) == 0:
        # print("No subprojects have been modified!")

    return targets
