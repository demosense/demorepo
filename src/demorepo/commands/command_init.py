import glob
import json
import os

from . import METADATA_PATH


def init(args):
    # Normalize project path (remove the last / if exists)
    args['path'] = os.path.normpath(args['path'])

    # Save the init json in the status folder.
    # The file contains one first level key for each monorepo configured with this tool.
    # If this key already exists, overwrite the metadata.

    # First, for the very first time, create the METADATA_PATH dirname folder
    if not os.path.exists(METADATA_PATH):
        os.makedirs(METADATA_PATH)

    # If the init.json file already exists, load it and update its information.
    if os.path.exists(os.path.join(METADATA_PATH, 'init.json')):
        with open(os.path.join(METADATA_PATH, 'init.json'), 'r') as f:
            metadata = json.loads(f.read())
    # Otherwise, we start from an empty init.json object
    else:
        metadata = {}

    abspath = os.getcwd()
    metadata[abspath] = {
        "last_init": {
            "args": args
        }
    }

    with open(os.path.join(METADATA_PATH, 'init.json'), 'w') as f:
        f.write(json.dumps(metadata))
