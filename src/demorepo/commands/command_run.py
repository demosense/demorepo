import yaml
import os
import sys
import subprocess
from . import ci
from .targets import append_dependencies


def _run_targets(projects_path, targets, stage, env):
    errors = []

    for t in targets:
        if not os.path.exists(os.path.join(projects_path, t, 'demorepo.yml')):
            print(f"demorepo.yml not found in target {t}. Skipping it.")
            continue

        with open(os.path.join(projects_path, t, 'demorepo.yml')) as f:
            demorepo_yml = yaml.load(f.read())

        if demorepo_yml is None or stage not in demorepo_yml:
            print(f"stage {stage} not found in demorepo.yml of target {t}. Skipping it.")
            continue

        script = demorepo_yml[stage]['script']

        child_environ = os.environ.copy()
        if env:
            for varset in env:
                var_name, var_value = varset.split("=")
                var_name = var_name.strip()
                var_value = var_value.strip()
                if var_value[0] == '$':
                    var_value = subprocess.run(f'echo {var_value}', shell=True, env=child_environ,
                                               stdout=subprocess.PIPE).stdout.decode().strip()
                child_environ[var_name] = var_value

        p = subprocess.run(script, shell=True, env=child_environ, cwd=os.path.join(projects_path, t),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = p.stdout.decode()
        stderr = p.stderr.decode()
        print(f"Script of stage {stage} has been executed.\nStdout: {stdout}.\nStderr: {stderr}")

        if p.returncode < 0:
            errors.append({t: f"Error executing the script of stage {stage}."})

    if len(errors) > 0:
        sys.exit(-1)


def run(args):
    projects_path = args['path']
    stage = args['stage']

    if args['all_targets'] or args.get('targets'):
        # target projects set manually
        if args['all_targets']:
            # _run_targets looks for demorepo.yml files: there is no need to filter by folders containing demorepo.yml
            targets = os.listdir(projects_path)
            print(f"All target projects are: {targets}")
        else:
            # strip each target to remove blank spaces, line breaks and other redundant chars
            targets = [t.strip() for t in args['targets'].split()]
            if args['recursive_deps']:
                targets = append_dependencies(targets, args)
                print(f"Target projects with dependencies are: {targets}")
    else:
        # Compute targets depending on the selected ci
        try:
            targets = ci.get_targets(args)
        except Exception as e:
            print(f"ERROR: Could not obtain target projects from ci-tool: {e}.")
            sys.exit(-1)

    # Now run the stage for target projects
    _run_targets(projects_path, targets, stage, args.get('env'))
