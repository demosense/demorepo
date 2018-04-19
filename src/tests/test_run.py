import pytest
import subprocess
import sys

from . import mock_subprocess_run, mock_sys_exit, mock_dict, setup
from demorepo import commands

default_args = {
    'working_mode': 'run-stage',
    'stage': 'test',
    'reverse_targets': False,
    'recursive_deps': False
}


def test_run_global_all(setup):

    args = default_args.copy()
    args["stage"] = "test-all"

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)

    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 2


def test_run_global_all_filter(setup):

    args = default_args.copy()
    args["stage"] = "test-all"
    args["targets"] = "p2"

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)

    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_global_all_filter_empty(setup):

    args = default_args.copy()
    args["stage"] = "test-all"
    args["targets"] = ""

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)

    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 0


def test_run_global_p2(setup):

    args = default_args.copy()
    args["stage"] = "test-p2"

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)

    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 1


def test_run_global_all_p3_fails(setup):

    args = default_args.copy()
    args["stage"] = "test-all-p3-fails"

    mock_dict['mock_subprocess_run'] = 0
    mock_dict['mock_sys_exit'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    setup.setattr(sys, 'exit', mock_sys_exit)

    commands.run_stage(args)

    assert mock_dict['mock_subprocess_run'] == 3
    assert mock_dict['mock_sys_exit'] == 1


def test_run_global_all_invalid(setup):

    args = default_args.copy()
    args["stage"] = "test-all-invalid"

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    with pytest.raises(Exception, match="Error: Unrecognized project p4 defined for stage test-all-invalid in global demorepo.yml"):
        commands.run_stage(args)


def test_run_all_local_p1(setup):
    # TODO: How can we really assert that this is really calling the local script?
    args = default_args.copy()
    args["stage"] = "test-all-local-p1"

    mock_dict['mock_subprocess_run'] = 0
    setup.setattr(subprocess, 'run', mock_subprocess_run)
    commands.run_stage(args)
    assert mock_dict['mock_subprocess_run'] == 2

# TODO: Test with different config and check execution order, reverse and cycles
# TODO: test inverse dependencies
# TODO: Test env variables in output
# TODO: Test run commands
