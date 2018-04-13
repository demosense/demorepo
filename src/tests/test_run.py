from demorepo import commands
import subprocess
from . import mock_subprocess_run, mock_sys_exit, mock_dict, setup
import sys


def test_run_test_from_citool(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': None,
        'reverse_targets': False,
        'ci_tool': 'gitlab',
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setenv('CI_COMMIT_REF_NAME', 'master')
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 2

# Deprecated!
# def test_run_deploy_from_citool(setup):
#     args = {
#         'working_mode': 'run-stage',
#         'path': 'tests/projects',
#         'stage': 'deploy',
#         'env': ['DEPLOY_VAR=DEPLOY_VAR', 'DEPLOY_ENV_VAR=$DEPLOY_ENV_VAR_VALUE'],
#         'targets': None,
#         'reverse_targets': False,
#         'ci_tool': 'gitlab',
#         'recursive_deps': False
#     }

#     mock_dict['mock_subprocess_run'] = 0
#     setup.setenv('CI_COMMIT_REF_NAME', 'master')
#     setup.setenv('DEPLOY_ENV_VAR_VALUE', 'Valor de DEPLOY_ENV_VAR_VALUE')
#     setup.setattr(subprocess, 'run', mock_subprocess_run)
#     commands.run_stage(args)
#     assert mock_dict['mock_subprocess_run'] == 2


def test_run_p1(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p1",
        'reverse_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_p1_recursive(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p1",
        'reverse_targets': False,
        'recursive_deps': True
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_p3_recursive(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p3",
        'reverse_targets': False,
        'recursive_deps': True
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 0


def test_run_p1_p3(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p1 p3",
        'reverse_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_p3(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p3",
        'reverse_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 0


def test_run_all(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'test',
        'reverse_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_command_all(setup):

    args = {
        'working_mode': 'run',
        'path': 'tests/projects',
        'command': 'echo "Hello world"',
        'reverse_targets': False,
        'targets': None,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 3


def test_run_command_p1_p2(setup):

    args = {
        'working_mode': 'run',
        'path': 'tests/projects',
        'env': ['VARIABLE=Something'],
        'command': 'echo "$VARIABLE else"',
        'targets': "p1 p2",
        'reverse_targets': False,
        'recursive_deps': False,
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_p3_fails(setup):

    args = {
        'working_mode': 'run-stage',
        'path': 'tests/projects',
        'stage': 'failure',
        'targets': "p3",
        'reverse_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    mock_dict['mock_sys_exit'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    setup.setattr(sys, 'exit', mock_sys_exit)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 1
    assert mock_dict['mock_sys_exit'] == 1
