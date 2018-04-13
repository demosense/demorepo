import sys
from . import ci
from .targets import append_dependencies

from . import METADATA_PATH


def lgc(args):
    # Compute targets depending on the selected ci
    try:
        targets = ci.get_targets(args)

        # print(f"Target projects with dependencies are: {targets}")

        # Print output projects to stdout
        print(" ".joint(targets))

    except Exception as e:
        print(
            f"ERROR: Could not obtain target projects from ci-tool: {e}.")
        sys.exit(-1)
