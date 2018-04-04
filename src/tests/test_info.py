from demorepo.commands import info
import os
import builtins
import yaml

mock_print_args_kwargs = []
def mock_return(*args):
    global mock_print_args_kwargs
    mock_print_args_kwargs += args

def test_info(monkeypatch):
    actual_path = os.getcwd()
    monkeypatch.setattr(os, 'getcwd', lambda: os.path.join(actual_path, 'tests'))
    monkeypatch.setattr(builtins, 'print', mock_return)
    with open('tests/config.yml') as f:
        config = yaml.load(f.read())

    args = {
        'command': 'info',
        'section': 'demorepo',
        'version': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["demorepo"]["version"]

    args = {
        'command': 'info',
        'section': 'demorepo',
        'version': False
    }
    info(args)
    assert mock_print_args_kwargs[-1] == "No valid option provided for info demorepo."

    args = {
        'command': 'info',
        'section': 'ci-tool',
        'name': True,
        'url': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["ci-tool"]["name"]

    args = {
        'command': 'info',
        'section': 'ci-tool',
        'name': False,
        'url': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["ci-tool"]["url"]

    args = {
        'command': 'info',
        'section': 'ci-tool',
        'name': False,
        'url': False
    }
    info(args)
    assert mock_print_args_kwargs[-1] == "No valid option provided for info ci-tool."

    args = {
        'command': 'info',
        'section': 'projects',
        'path': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["projects"]["path"]

    args = {
        'command': 'info',
        'section': 'projects',
        'path': False
    }
    info(args)
    assert mock_print_args_kwargs[-1] == "No valid option provided for info projects."


