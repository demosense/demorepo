from collections import defaultdict

from demorepo import logger


__all__ = ['get_targets']


def get_targets(targets, dependencies, targets_filter, reverse_targets=False, inverse_dependencies=False):

    if targets_filter is not None:
        # If filter is empty it means that we will return an empty list so nothing gets run
        if targets_filter == "":
            return []

        # Strip each target to remove blank spaces, line breaks and other redundant chars
        targets_filter = [t.strip() for t in targets_filter.split()]
        # Filter if target present in args
        if targets_filter:
            for t in targets_filter:
                if t not in targets:
                    raise Exception(
                        "Unrecognized project {} in --targets".format(t))
            targets = [t for t in targets if t in targets_filter]

    # Set reverse dependency targets if inverse_dependencies
    if inverse_dependencies:
        targets = _add_inverse_dependencies(targets, dependencies)

    # Set target order
    targets = _order_targets(targets, dependencies)

    # Reverse if specified in args
    if reverse_targets:
        targets.reverse()

    logger.info("Target projects are: {}".format(targets))

    return targets


def _order_targets(targets, dependencies):
    ordered = []
    candidates = targets

    i = 0
    while candidates:
        for t in candidates:
            if not set(dependencies[t]).intersection(set(candidates)):
                ordered.append(t)

        candidates = [c for c in candidates if c not in set(ordered)]
        i += 1
        if i > len(targets):
            raise Exception("Error: Cyclic dependency in projects")

    return list(ordered)


def _add_inverse_dependencies(targets, dependencies):
    # Process the dict of dependents (projects which are dependent of a project; inverse of dependencies)
    dependents = defaultdict(set)
    for project in dependencies:
        for dependency in dependencies[project]:
            dependents[dependency].add(project)

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
