import yaml
import os
import sys
import json
import subprocess
from . import METADATA_PATH


def _run_targets(projects_path, targets, stage, env):
    errors = []

    for t in targets:
        if not os.path.exists(os.path.join(projects_path, t, 'demorepo.yml')):
            print(f"demorepo.yml not found in target {t}. Skipping it.")
            continue

        print(t)
        with open(os.path.join(projects_path, t, 'demorepo.yml')) as f:
            demorepo_yml = yaml.load(f.read())

        if demorepo_yml is None or stage not in demorepo_yml:
            print(f"stage {stage} not found in demorepo.yml of target {t}. Skipping it.")
            continue

        script = demorepo_yml[stage]['script']

        child_environ = os.environ.copy()
        if env:
            child_environ["DEMOREPO_ENV"] = env

        p = subprocess.run(script.split(), env=child_environ, cwd=os.path.join(projects_path, t),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = p.stdout.decode()
        stderr = p.stderr.decode()
        print(f"Script of stage {stage} has been executed.\nStdout: {stdout}.\nStderr: {stderr}")

        if p.returncode < 0:
            errors.append({t: f"Error executing the script of stage {stage}."})

    if len(errors) > 0:
        sys.exit(-1)


def run(args):
    stage = args['stage']

    if args['all-targets'] or 'targets' in args:
        # Targets selected manually. It must exists 'path' too
        if 'path' not in args:
            print("If --targets are set manually, --path argument must exist too.")
            sys.exit(-1)

        projects_path = args['path']

        if args['all-targets']:
            targets = os.listdir(projects_path)
        else:
            # strip each target to remove blank spaces, line breaks and other redundant chars
            targets = [t.strip() for t in args['targets'].split()]

        _run_targets(projects_path, targets, stage, args.get('env'))

    elif os.path.exists(os.path.join(METADATA_PATH, 'init.json')):
        with open(os.path.join(METADATA_PATH, 'init.json')) as f:
            init_json = json.loads(f.read())
        if os.getcwd() not in init_json:
            print("Init command has never been executed in this path. "
                  "Run init command before, or provide --targets and --path arguments.")
            sys.exit(-1)
        projects_path = init_json[os.getcwd()]["last_init"]["args"]["path"]
        targets = init_json[os.getcwd()]["last_init"]["targets"]

        _run_targets(projects_path, targets, stage, args.get('env'))

    else:
        print("Run init command before, or provide --targets and --path arguments.")
        sys.exit(-1)
