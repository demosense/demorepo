import os

from demorepo import logger
from demorepo import parser
from .command_run import run, run_stage
from .command_lgc import lgc
from .command_diff import diff

__all__ = ['exec_command']


def exec_command(args):
    # set the logger configuration
    if not args['silent']:
        logger.add_console_handler()

    if args['log_path']:
        logger.add_file_handler(args['log_path'])
    elif args['working_mode'] == 'lgc':
        lgc(args)
    elif args['working_mode'] == 'diff':
        diff(args)
    elif args['working_mode'] == 'run':
        run(args)
    elif args['working_mode'] == 'run-stage':
        run_stage(args)
    else:
        parser.print_help()
