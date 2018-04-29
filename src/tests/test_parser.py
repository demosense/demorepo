import pytest
import sys
from . import raises

from demorepo import parser

defaults = dict(silent=False, log_path=None, working_mode=None)
lgc_defaults = dict(ci_tool='gitlab', ci_url=None)
run_defaults = dict(targets=None, env=None, reverse_targets=False, stop_on_error=False, inverse_dependencies=False)
stage_defaults = dict(targets=None, env=None, reverse_targets=False, stop_on_error=False, inverse_dependencies=False)


@pytest.mark.parametrize("argv,expected,exit", [
    # No argument, should print exit
    # TODO: check print help
    (
        ['demorepo'],
        dict(defaults),
        None
    ),
    # Unrecognized command should exit
    (
        ['demorepo', 'this does not exist'],
        dict(defaults),
        SystemExit
    ),
    # lgc defaults
    (
        ['demorepo', 'lgc'],
        dict(defaults, working_mode='lgc', **lgc_defaults),
        None,
    ),
    # diff required
    (
        ['demorepo', 'diff', 'HEAD'],
        dict(defaults, working_mode='diff', sha='HEAD'),
        None,
    ),
    # diff Missing required
    (
        ['demorepo', 'diff'],
        dict(defaults, working_mode='diff'),
        SystemExit,
    ),
    # run required
    (
        ['demorepo', 'run', 'ls'],
        dict(defaults, working_mode='run', command='ls', **run_defaults),
        None,
    ),
    # run required fail
    (
        ['demorepo', 'run'],
        dict(defaults, working_mode='run', **run_defaults),
        SystemExit,
    ),
    # run opts
    (
        ['demorepo', 'run', 'ls', '--targets', 'target1', '--reverse-targets',
         '--stop-on-error', '--env', 'cosa=1234', '--inverse-dependencies'],
        dict(defaults, working_mode='run', command='ls', targets='target1',
             reverse_targets=True, stop_on_error=True, env=['cosa=1234'], inverse_dependencies=True),
        None,
    ),
    # stage required
    (
        ['demorepo', 'stage', 'deploy'],
        dict(defaults, working_mode='stage', stage='deploy', **stage_defaults),
        None,
    ),
    # stage required fail
    (
        ['demorepo', 'stage'],
        dict(defaults, working_mode='stage', **stage_defaults),
        SystemExit,
    ),
    # stage opts
    (
        ['demorepo', 'stage', 'deploy', '--targets', 'target1', '--reverse-targets',
         '--stop-on-error', '--env', 'cosa=1234', '--inverse-dependencies'],
        dict(defaults, working_mode='stage', stage='deploy', targets='target1',
             reverse_targets=True, stop_on_error=True, env=['cosa=1234'], inverse_dependencies=True),
        None,
    ),
])
def test_parser(argv, expected, exit, monkeypatch):
    monkeypatch.setattr(sys, 'argv', argv)
    with raises(exit):
        args = parser.parse_args()
        print(args)
        print(expected)
        assert args == expected
