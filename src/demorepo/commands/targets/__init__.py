from demorepo import logger


__all__ = ['get_targets']


def get_targets(targets, dependencies, targets_filter, reverse_targets=False, recursive_deps=False):

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

    # Set target order
    targets = _order_targets(targets, dependencies)

    # Reverse if specified in args
    if (reverse_targets):
        targets.reverse()

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


def _add_deps(targets, dependencies, projects):
    # TODO: Implement inverse dependencies with projects
    pass
