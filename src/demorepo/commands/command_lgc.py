import sys
from . import ci


def lgc(args):

    ci_tool = args.get("ci_tool")
    ci_url = args.get("ci-url", None)

    # Compute targets depending on the selected ci
    try:
        last_green_commit = ci.get_lgc(ci_tool, ci_url)

        print(last_green_commit)

    except Exception as e:
        print("ERROR: Could not obtain lgc from ci-tool: {}.".format(e))
        sys.exit(-1)
