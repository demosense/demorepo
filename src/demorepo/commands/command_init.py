import subprocess
import os
import sys
import glob
import json
from . import gitlab

SCRIPTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts/gitlab')
METADATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata/init.json')


def filter_targets(targets, args):
    """
    Filter the projects in targets (names of modified projects) which has been deleted or does not contain the
    file demorepo.yml (in this case, not considered a project of this demorepo).
    :param targets: A list of names of modified projects with respect to the last green commit.
    :param args: The dict with the parser argument.
    :return: The filtered names of modified projects (not deleted and considered demorepo projects).
    """
    # Remove all the subprojects in modified_subprojects which does not exists:
    return [t for t in targets if os.path.isdir(
        os.path.join(args['target'], t)) and os.path.exists(os.path.join(args['target'], t, 'demorepo.yml'))]


def append_dependencies(targets, args):
    """
    Only implemented for python projects. Search for requirements files and include those projects which depends on
    a modified project (target).
    :param targets: A list of names of modified projects with respect to the last green commit.
    :param args: The dict with the parser argument.
    :return: The projects which has been modified from last green commit of have modified dependencies
    """
    # Get the all the project paths (which are folders). *Only the names*.
    all_project_names = [f for f in os.listdir(args['target']) if os.path.isdir(os.path.join(args['target'], f))]

    # Just extend the python projects, where a requirements file is inside
    python_project_names = [f for f in all_project_names
                            if len(glob.glob(os.path.join(args['target'], f, 'requirements*'))) > 0]


    # Process the dict of dependents (projects which are dependent of a project; inverse of requirements)
    dependents = dict()
    for sub1 in python_project_names:
        dependents[sub1] = []
        # Always use relative paths. Wherever the subprojects folder is, the subprojects are always in "../"
        # Match exactly with "git+file://../$sub1". If using other branch i.e.: "...$sub1@release/1.0",
        # the modification of $sub1 (in the actual commit) does not affect to the $sub2 project
        # (requirements refers to other commit code)
        requirements_line = "../" + sub1.strip()  # strip to remove any possible whitespaces or line breaks
        for sub2 in python_project_names:
            requirements_paths = glob.glob(f"{os.path.join(args['target'], sub2)}/requirements*")
            if any(requirements_line == l.strip() for req_path in requirements_paths
                   for l in open(req_path).readlines()):
                dependents[sub1].append(sub2)

    # This recursive function add the dependencies in the set s when e is marked as modified
    def add_dependencies(e, s):
        new_elements = [x for x in dependents[e] if x not in s]
        for n in new_elements:
            s.add(n)
            add_dependencies(n, s)

    # Now, for each modified project, get its name (to use the dependents dict) and add its dependencies
    s = set()
    modified_names = [m[(m.rfind('/') + 1):] for m in targets]
    for m in modified_names:
        s.add(m)
        add_dependencies(m, s)

    # Return the extended list of target projects
    return list(s)


def init(args):
    # Normalize project path (remove the last / if exists)
    args['target'] = os.path.normpath(args['target'])

    # Depending on the ci_tool option, run the respective function
    if args["ci_tool"] == "gitlab":
        targets = init_gitlab(args)

    # Save the init json in the status folder. It will be used by the other commands.
    # The file contains one first level key for each monorepo configured with this tool (using the abs path where
    # this CLI has been executed). If this key already exists, overwrite the metadata.

    # First, for the very first time, create the METADATA_PATH dirname folder
    if not os.path.exists(os.path.dirname(METADATA_PATH)):
        os.makedirs(os.path.dirname(METADATA_PATH))

    # If the init.json file already exists, load it and update its information.
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as f:
            metadata = json.loads(f.read())
    # Otherwise, we start from an empty init.json object
    else:
        metadata = {}

    abspath = os.getcwd()
    metadata[abspath] = {
        "last_init": {
            "args": args,
            "targets": targets
        }
    }

    with open(METADATA_PATH, 'w') as f:
        f.write(json.dumps(metadata))


def init_gitlab(args):
    # Clone the actual environ (contains required env vars) and append new ones for the child process
    child_environ = os.environ.copy()
    child_environ["CI_SERVER_URL"] = args.get('ci-url') or gitlab.defaults["CI_SERVER_URL"]
    child_environ["PROJECTS_PATH"] = args['target']

    targets = gitlab.get_target_projects(child_environ)

    # TARGET_SUBPROJECTS might contain residual folders or files. A project should be a folder with the
    # demorepo.yml file inside. Also, it might contain even deleted subprojects (are git differences!).
    # Remove them if they do not exist.
    targets = filter_targets(targets, args)
    print(f"Filtered target projects are: {targets}")

    # If argument recursive_deps is True, we include in the targets the dependencies of the modified projects (targets)
    # NOTE: Actually this is only implemented for Python projects, based on requirements file dependencies.
    # Python dependencies process:
    # This is a recursive process which checks any requirements.* file inside each project.

    if args['recursive_deps']:
        targets = append_dependencies(targets, args)
        print(f"Target projects with dependencies are: {targets}")

    if len(targets) == 0:
        print("No subprojects have been modified!")

    return targets
