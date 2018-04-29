import pytest
import sys
from . import raises

from demorepo import parser

defaults = dict(silent=False, log_path=None, working_mode=None)
lgc_defaults = dict(ci_tool='gitlab', ci_url=None)
run_defaults = dict(targets=None, env=None, reverse_targets=False)
stage_defaults = dict(targets=None, env=None, reverse_targets=False)


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
    # diff required A
    (
        ['demorepo', 'diff', '-s', 'HEAD'],
        dict(defaults, working_mode='diff', sha='HEAD'),
        None,
    ),
    # diff required B
    (
        ['demorepo', 'diff', '--sha', 'HEAD'],
        dict(defaults, working_mode='diff', sha='HEAD'),
        None,
    ),
    # diff Missing required
    (
        ['demorepo', 'diff'],
        dict(defaults, working_mode='diff'),
        SystemExit,
    ),
    # run required A
    (
        ['demorepo', 'run', '-c', 'ls'],
        dict(defaults, working_mode='run', **run_defaults, command='ls'),
        None,
    ),
    # run required B
    (
        ['demorepo', 'run', '--command', 'ls'],
        dict(defaults, working_mode='run', **run_defaults, command='ls'),
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
        ['demorepo', 'run', '--command', 'ls', '--targets', 'target1', '--reverse-targets', '--env', 'cosa=1234'],
        dict(defaults, working_mode='run', command='ls', targets='target1', reverse_targets=True, env=['cosa=1234']),
        None,
    ),
    # stage required A
    (
        ['demorepo', 'stage', '-s', 'deploy'],
        dict(defaults, working_mode='stage', **stage_defaults, stage='deploy'),
        None,
    ),
    # stage required B
    (
        ['demorepo', 'stage', '--stage', 'deploy'],
        dict(defaults, working_mode='stage', **stage_defaults, stage='deploy'),
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
        ['demorepo', 'stage', '--stage', 'deploy', '--targets', 'target1', '--reverse-targets', '--env', 'cosa=1234'],
        dict(defaults, working_mode='stage', stage='deploy',
             targets='target1', reverse_targets=True, env=['cosa=1234']),
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
