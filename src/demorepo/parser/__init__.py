import argparse
import sys
__all__ = ['parse_args', 'print_help']


# demorepo
parser = argparse.ArgumentParser(prog='demorepo',
                                 description='Tool to manage a monorepo, where projects can be general projects '
                                 '(language code, build and test management...).')

# demorepo arguments to handle the logger options
parser.add_argument('--silent', action='store_true', help='Text is not printed to stdout')
parser.add_argument('--log-path', help='Text is written to a file path')

subparsers = parser.add_subparsers(title='working mode', description='init, run or integration',
                                   help='working mode to group commands based on it.',
                                   dest='working_mode')

#
# demorepo lgc
parser_lgc = subparsers.add_parser('lgc',
                                   description='Return the last green commit according to the configured '
                                   'ci tool in the config file or by option --ci-tool')

parser_lgc.add_argument('--ci-tool', default='gitlab', choices=['gitlab'],
                        help='The specific CI tool (e.g.: gitlab, Circle-CI, ....)')
parser_lgc.add_argument(
    '--ci-url', help='the URL to the CI Server. By default uses the general public URL.')

#
# demorepo diff
parser_diff = subparsers.add_parser('diff',
                                    description='Return the projects that have changed according to the provided sha')
parser_diff.add_argument(
    '-s', '--sha', required=True, help='SHA of the commit to compare with')

#
# demorepo run-stage
parser_run_stage = subparsers.add_parser('run-stage',
                                         description='Run the specified stage in the global and local config files.')
parser_run_stage.add_argument(
    '-s', '--stage', required=True, help='Stage name in the project demorepo.yml')
parser_run_stage.add_argument('-e', '--env', action='append', help='Optional variables passed to the target stage script.'
                              ' The format is VAR_NAME=VAR_VALUE. '
                              'Multiple env vars can be specified.')
# parser_run_stage.add_argument('-r', '--recursive-deps', action='store_true',
#                               help='Find projects recursively which depends on target projects and include them as '
#                               'target projects too.')
parser_run_stage.add_argument('-t', '--targets', help='A list of target project names to run the provided stage, '
                              'separated by blank spaces (use quotes around the string).')
parser_run_stage.add_argument('--reverse-targets', action='store_true',
                              help='Reverse the dependency order for projects')

#
# demorepo run
parser_run = subparsers.add_parser('run',
                                   description='Execute a shell command for all projects.')
parser_run.add_argument('-c', '--command', required=True,
                        help='The shell command to execute.')
parser_run.add_argument('-t', '--targets', help='A list of target project names to run the provided stage, '
                        'separated by blank spaces (use quotes around the string).')
parser_run.add_argument('-e', '--env', action='append',
                        help='Optional variables passed to the target stage script.'
                        ' The format is VAR_NAME=VAR_VALUE. '
                        'Multiple env vars can be specified.')
# parser_run.add_argument('-r', '--recursive-deps', action='store_true',
#                               help='Find projects recursively which depends on target projects and include them as '
#                                    'target projects too.')
parser_run.add_argument('--reverse-targets', action='store_true',
                        help='Reverse the dependency order for projects')

#
# End commands
#


def parse_args():
    args = vars(parser.parse_args())
    return args


def print_help():
    parser.print_help()