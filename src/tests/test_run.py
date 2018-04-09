from demorepo import commands
import subprocess
from . import mock_subprocess_run, mock_sys_exit, mock_dict, setup
import sys


def test_run_test_from_citool(setup):

    args = {
        'command': 'run',
        'path' : 'tests/projects',
        'stage': 'test',
        'targets': None,
        'all_targets': False,
        'ci_tool': 'gitlab',
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setenv('CI_COMMIT_REF_NAME', 'master')
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_deploy_from_citool(setup):
    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'deploy',
        'env': ['DEPLOY_VAR=DEPLOY_VAR', 'DEPLOY_ENV_VAR=$DEPLOY_ENV_VAR_VALUE'],
        'targets': None,
        'all_targets': False,
        'ci_tool': 'gitlab',
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setenv('CI_COMMIT_REF_NAME', 'master')
    setup.setenv('DEPLOY_ENV_VAR_VALUE', 'Valor de DEPLOY_ENV_VAR_VALUE')
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_p1(setup):

    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p1",
        'all_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_p1_recursive(setup):

    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p1",
        'all_targets': False,
        'recursive_deps': True
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_p3_recursive(setup):

    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p3",
        'all_targets': False,
        'recursive_deps': True
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 0


def test_run_p1_p3(setup):

    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p1 p3",
        'all_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_p3(setup):

    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p3",
        'all_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 0


def test_run_all(setup):

    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'test',
        'targets': "p2",
        'all_targets': True
    }

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_p3_fails(setup):

    args = {
        'command': 'run',
        'path': 'tests/projects',
        'stage': 'failure',
        'targets': "p3",
        'all_targets': False,
        'recursive_deps': False
    }

    mock_dict['mock_subprocess_run'] = 0
    mock_dict['mock_sys_exit'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    setup.setattr(sys, 'exit', mock_sys_exit)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1
    assert mock_dict['mock_sys_exit'] == 1
