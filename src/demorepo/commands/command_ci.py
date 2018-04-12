import sys
from . import ci as ci_module
from .targets import append_dependencies

from . import METADATA_PATH


def ci(args):
    # Compute targets depending on the selected ci
    try:
        targets = ci_module.get_targets(args)
        if args['recursive_deps']:
            targets = append_dependencies(targets, args)
        print(f"Target projects with dependencies are: {targets}")
        return targets
    except Exception as e:
        print(f"ERROR: Could not obtain target projects from ci-tool: {e}.")
        sys.exit(-1)
