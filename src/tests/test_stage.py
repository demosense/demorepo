import pytest
import subprocess
import sys

from . import mock_subprocess_Popen, mock_sys_exit, mock_dict, setup
from demorepo import commands

default_args = {
    'working_mode': 'stage',
    'stage': 'test',
    'targets': None,
    'reverse_targets': False,
    'stop_on_error': True,
    'inverse_dependencies': False
}


def test_run_all(setup):

    args = default_args.copy()
    args["stage"] = "test-all"

    mock_dict['mock_subprocess_Popen'] = 0
    setup.setattr(subprocess, 'Popen', mock_subprocess_Popen)

    commands.stage(args)
    assert mock_dict['mock_subprocess_Popen'] == 2


def test_run_all_filter(setup):

    args = default_args.copy()
    args["stage"] = "test-all"
    args["targets"] = "p2"

    mock_dict['mock_subprocess_Popen'] = 0
    setup.setattr(subprocess, 'Popen', mock_subprocess_Popen)

    commands.stage(args)
    assert mock_dict['mock_subprocess_Popen'] == 1


def test_run_all_filter_empty(setup):

    args = default_args.copy()
    args["stage"] = "test-all"
    args["targets"] = ""

    mock_dict['mock_subprocess_Popen'] = 0
    setup.setattr(subprocess, 'Popen', mock_subprocess_Popen)

    commands.stage(args)
    assert mock_dict['mock_subprocess_Popen'] == 0


def test_run_global_p2(setup):

    args = default_args.copy()
    args["stage"] = "test-p2"

    mock_dict['mock_subprocess_Popen'] = 0
    setup.setattr(subprocess, 'Popen', mock_subprocess_Popen)

    commands.stage(args)
    assert mock_dict['mock_subprocess_Popen'] == 1


def test_run_global_all_p3_fails(setup):

    args = default_args.copy()
    args["stage"] = "test-all-p3-fails"

    mock_dict['mock_subprocess_Popen'] = 0
    mock_dict['mock_sys_exit'] = 0
    setup.setattr(subprocess, 'Popen', mock_subprocess_Popen)
    setup.setattr(sys, 'exit', mock_sys_exit)

    commands.stage(args)

    assert mock_dict['mock_subprocess_Popen'] == 3
    assert mock_dict['mock_sys_exit'] == 1


def test_run_all_p1_interrupts(setup):

    args = default_args.copy()
    args["stage"] = "test-all-p1-interrupts"

    mock_dict['mock_subprocess_Popen'] = 0
    mock_dict['mock_sys_exit'] = 0
    setup.setattr(subprocess, 'Popen', mock_subprocess_Popen)
    setup.setattr(sys, 'exit', mock_sys_exit)

    commands.stage(args)

    assert mock_dict['mock_subprocess_Popen'] == 1
    assert mock_dict['mock_sys_exit'] == 1


def test_run_all_local_p1(setup):
    # TODO: How can we really assert that this is really calling the local script?
    args = default_args.copy()
    args["stage"] = "test-all-local-p1"

    mock_dict['mock_subprocess_Popen'] = 0
    setup.setattr(subprocess, 'Popen', mock_subprocess_Popen)
    commands.stage(args)
    assert mock_dict['mock_subprocess_Popen'] == 2

# TODO: Test with different config and check execution order, reverse and cycles
# TODO: test inverse dependencies
# TODO: Test env variables in output
# TODO: Test run commands
