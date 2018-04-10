from demorepo.commands import info
import builtins
import yaml
from . import setup

mock_print_args_kwargs = []
def mock_return(*args):
    global mock_print_args_kwargs
    mock_print_args_kwargs += args

def test_info(setup):
    setup.setattr(builtins, 'print', mock_return)
    with open('tests/config.yml') as f:
        config = yaml.load(f.read())

    args = {
        'working_mode': 'info',
        'section': 'demorepo',
        'version': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["demorepo"]["version"]

    args = {
        'working_mode': 'info',
        'section': 'demorepo',
        'version': False
    }
    info(args)
    assert mock_print_args_kwargs[-1] == "No valid option provided for info demorepo."

    args = {
        'working_mode': 'info',
        'section': 'ci-tool',
        'name': True,
        'url': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["ci-tool"]["name"]

    args = {
        'working_mode': 'info',
        'section': 'ci-tool',
        'name': False,
        'url': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["ci-tool"]["url"]

    args = {
        'working_mode': 'info',
        'section': 'ci-tool',
        'name': False,
        'url': False
    }
    info(args)
    assert mock_print_args_kwargs[-1] == "No valid option provided for info ci-tool."

    args = {
        'working_mode': 'info',
        'section': 'projects',
        'path': True,
        'order': False
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["projects"]["path"]

    args = {
        'working_mode': 'info',
        'section': 'projects',
        'path': False,
        'order': True
    }
    info(args)
    assert mock_print_args_kwargs[-1] == config["projects"]["order"]

    args = {
        'working_mode': 'info',
        'section': 'projects',
        'path': False,
        'order': False
    }
    info(args)
    assert mock_print_args_kwargs[-1] == "No valid option provided for info projects."


