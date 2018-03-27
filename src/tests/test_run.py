from demorepo import commands
import subprocess
from . import setup_run_init, mock_subprocess_run, mock_dict


def test_run_test_from_init(setup_run_init, monkeypatch):

    args = {
        'command': 'run',
        'stage': 'test'
    }

    mock_dict['mock_subprocess_run'] = 0
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_deploy_from_init(setup_run_init, monkeypatch):
    args = {
        'command': 'run',
        'stage': 'deploy',
        'env': 'DEPLOY_VAR'
    }

    mock_dict['mock_subprocess_run'] = 0
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_p1_p2(setup_run_init, monkeypatch):

    args = {
        'command': 'run',
        'stage': 'test',
        'path': 'tests/projects',
        'targets': "p1 p2"
    }

    mock_dict['mock_subprocess_run'] = 0
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_p3(setup_run_init, monkeypatch):

    args = {
        'command': 'run',
        'stage': 'test',
        'path': 'tests/projects',
        'targets': "p3"
    }

    mock_dict['mock_subprocess_run'] = 0
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 0
