import os
import subprocess
import sys
import yaml

from demorepo import config
from demorepo import logger
from demorepo import strformat
from .targets import get_targets


def _get_scripts(projects, paths, stage, targets):

    # Accumulator
    scripts = {}

    # Load stages from global demorepo
    # Parse global file
    global_stages_path = os.path.join(os.getcwd(), 'demorepo.yml')
    if os.path.exists(global_stages_path):
        with open(global_stages_path) as f:
            global_config = yaml.load(f.read())

            # If the stage is defined in the global stage, capture the projects
            if stage in global_config:
                script = global_config[stage]['script']
                included_projects = global_config[stage]['projects']

                # Check if projects are defined
                for p in [p for p in included_projects if p not in projects]:
                    raise Exception(
                        "Error: Unrecognized project {} defined for stage {} in global demorepo.yml".format(p, stage))

                # Assign the script for each valid target
                scripts = {
                    p: script for p in included_projects if p in targets}

            else:
                logger.error("Stage {} not defined in global demorepo.yml".format(stage))
    else:
        logger.error("Global demorepo.yml not found")

    # Load stages from local demorepo
    for t in targets:
        local_stages_path = os.path.join(
            os.getcwd(), paths[t], 'demorepo.yml')
        if not os.path.exists(local_stages_path):
            continue

        with open(local_stages_path) as f:
            local_config = yaml.load(f.read())

        if stage in local_config:
            script = local_config[stage]['script']
            if t in scripts:
                logger.info("Overriding with local stage for target {}".format(t))

            scripts[t] = script

    return scripts


def _get_child_environ(env):
    child_environ = os.environ.copy()
    if env:
        for varset in env:
            var_name, var_value = varset.split("=")
            var_name = var_name.strip()
            var_value = var_value.strip()
            if var_value[0] == '$':
                var_value = subprocess.run('echo {}'.format(var_value), shell=True, env=child_environ,
                                           stdout=subprocess.PIPE).stdout.decode().strip()
            child_environ[var_name] = var_value
    return child_environ


def _run_targets(projects, paths, targets, env, *, stage=None, command=None):
    errors = []

    # Get scripts from stage scripts or paste the command
    if stage:
        scripts = _get_scripts(projects, paths, stage, targets)
    else:
        scripts = {t: command for t in targets}

    child_environ = _get_child_environ(env)

    for t, script in scripts.items():

        if stage is not None:
            logger.info("Running script of stage {} for target {}...".format(stage, t))
        else:
            logger.info("Running custom script for target {}...".format(t))


        p = subprocess.Popen(script, shell=True, env=child_environ, cwd=os.path.join(os.getcwd(), paths[t]),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # log the stdout as a stream in real-time (by lines)
        logger.info('')
        logger.info("Stdout:")
        while True:
            line = p.stdout.readline().decode().strip()
            if line == '' and p.poll() is not None:
                break
            if line:
                logger.info('>> {}'.format(line))

        stderr = p.communicate()[1].decode().strip()
        # log the stderr at the end (not in real-time)
        logger.info('')
        logger.info("Stderr:")
        for line in stderr.split('\n'):
            logger.info('>> {}'.format(line))

        if p.returncode != 0:
            errors.append(
                {t: "Error executing the script of stage {}.".format(stage)})

        logger.info('')
        logger.info(strformat.hline)

    if len(errors) > 0:
        logger.error("Errors running scripts in this stage. Printing them as key: [list of errors]:")
        logger.error(str(errors))
        sys.exit(-1)


def run_stage(args):
    stage = args['stage']
    targets = args.get('targets', None)
    reverse_targets = args['reverse_targets']
    env = args.get('env')

    projects = config.get_projects()
    dependencies = config.get_projects_dependencies()
    paths = config.get_projects_paths()

    targets = get_targets(projects, dependencies, targets, reverse_targets)
    _run_targets(projects, paths, targets, env, stage=stage)


def run(args):
    command = args['command']
    targets = args.get('targets', None)
    reverse_targets = args['reverse_targets']
    env = args.get('env')

    projects = config.get_projects()
    dependencies = config.get_projects_dependencies()
    paths = config.get_projects_paths()

    targets = get_targets(projects, dependencies, targets, reverse_targets)
    _run_targets(projects, paths, targets, env, command=command)
