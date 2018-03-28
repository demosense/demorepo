from demorepo import commands
import subprocess
from . import setup_run_init, mock_subprocess_run, mock_dict


def test_run_test_from_init(setup_run_init, monkeypatch):

    args = {
        'command': 'run',
        'stage': 'test',
        'all-targets': False
    }

    mock_dict['mock_subprocess_run'] = 0
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_deploy_from_init(setup_run_init, monkeypatch):
    args = {
        'command': 'run',
        'stage': 'deploy',
        'env': 'DEPLOY_VAR',
        'all-targets': False
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
        'targets': "p1 p2",
        'all-targets': False
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
        'targets': "p3",
        'all-targets': False
    }

    mock_dict['mock_subprocess_run'] = 0
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 0


def test_run_all(setup_run_init, monkeypatch):

    args = {
        'command': 'run',
        'stage': 'test',
        'path': 'tests/projects',
        'targets': "p2",
        'all-targets': True
    }

    mock_dict['mock_subprocess_run'] = 0
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run(args)
    assert mock_dict['mock_subprocess_run'] == 1
