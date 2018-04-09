import os
import glob


__all__ = ['filter_targets', 'append_dependencies']


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
        os.path.join(args['path'], t)) and os.path.exists(os.path.join(args['path'], t, 'demorepo.yml'))]


def append_dependencies(targets, args):
    """
    Only implemented for python projects. Search for requirements files and include those projects which depends on
    a modified project (target).
    :param targets: A list of names of modified projects with respect to the last green commit.
    :param args: The dict with the parser argument.
    :return: The projects which has been modified from last green commit of have modified dependencies
    """
    # Get the all the project paths (which are folders). *Only the names*.
    all_project_names = [f for f in os.listdir(args['path']) if os.path.isdir(os.path.join(args['path'], f))]

    # Just extend the python projects, where a requirements file is inside
    python_project_names = [f for f in all_project_names
                            if len(glob.glob(os.path.join(args['path'], f, 'requirements*'))) > 0]


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
            requirements_paths = glob.glob(f"{os.path.join(args['path'], sub2)}/requirements*")

            for req_path in requirements_paths:
                with open(req_path) as f:
                    if any(requirements_line == l.strip() for l in f.readlines()):
                        dependents[sub1].append(sub2)
                        break

    # This recursive function add the dependencies in the set s when e is marked as modified
    def add_dependencies(e, s):
        new_elements = [x for x in dependents[e] if x not in s]
        for n in new_elements:
            s.add(n)
            add_dependencies(n, s)

    # Now, for each modified project, get its name (to use the dependents dict) and add its dependencies
    s = set()
    for m in targets:
        s.add(m)
        # only if project is in dependents list (recursive option implemented for this project type)
        if m in dependents:
            add_dependencies(m, s)

    # Return the extended list of target projects
    return list(s)