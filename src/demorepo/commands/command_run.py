import yaml
import os
import sys
import subprocess
from .targets import get_targets, append_dependencies


def _run_targets(projects_path, targets, reverse_targets, env, *, stage=None, command=None):
    errors = []
    # apply the order to the targets list, just if config.yml exists in root path
    config_path = os.path.join(os.getcwd(), 'config.yml')
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = yaml.load(f.read())
        # get ordered list from projects field. If do not exists, use an empty list
        order_list = config["projects"].get("order", [])
        not_ordered_t = [t for t in targets if t not in order_list]
        # in this case, the order is the same as in order_list
        ordered_t = [t for t in order_list if t in targets]
        targets = ordered_t + not_ordered_t

        if (reverse_targets):
            targets.reverse()

        print(f"targets has been ordered: {targets}")

    for t in targets:
        if not os.path.exists(os.path.join(projects_path, t, 'demorepo.yml')):
            print(f"demorepo.yml not found in target {t}. Skipping it.")
            continue

        if stage is not None:
            with open(os.path.join(projects_path, t, 'demorepo.yml')) as f:
                demorepo_yml = yaml.load(f.read())

            if demorepo_yml is None or stage not in demorepo_yml:
                print(
                    f"stage {stage} not found in demorepo.yml of target {t}. Skipping it.")
                continue

            script = demorepo_yml[stage]['script']
        else:
            script = command

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

        if stage is not None:
            print(f"Script of stage {stage} has been executed.")
            print("Stdout:")
            print("=" * 20)
            print(stdout)
            print("Stderr:")
            print("=" * 20)
            print(stderr)
        else:
            print("Custom script has been executed.")
            print("Stdout:")
            print("=" * 20)
            print(stdout)
            print("Stderr:")
            print("=" * 20)
            print(stderr)

        if p.returncode != 0:
            errors.append({t: f"Error executing the script of stage {stage}."})

    if len(errors) > 0:
        print(
            "Errors running scripts in this stage. Printing them as key: [list of errors]:")
        print(errors)
        sys.exit(-1)


def run_stage(args):
    projects_path = args['path']
    stage = args['stage']
    targets = get_targets(args)
    reverse_targets = args['reverse_targets']

    _run_targets(projects_path, targets, reverse_targets,
                 args.get('env'), stage=stage)


def run(args):
    projects_path = args['path']
    command = args['command']
    targets = get_targets(args)
    reverse_targets = args['reverse_targets']

    # Now run the command for target projects
    _run_targets(projects_path, targets, reverse_targets,
                 args.get('env'), command=command)
