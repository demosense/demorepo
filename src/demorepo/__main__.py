import argparse
import os
from git import Repo
import demorepo.commands as commands


__package__ = "demorepo"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='demorepo',
                                     description='Tool to manage a monorepo, where projects can be general projects '
                                                 '(language code, build and test management...).')

    subparsers = parser.add_subparsers(title='working mode', description='init, run or integration',
                                       help='working mode to group commands based on it.',
                                       dest='working_mode')

    parser_init = subparsers.add_parser('init', description="Register a git repository in demorepo package.")
    # TODO: Complete the init part. Useful?

    parser_info = subparsers.add_parser('info', description="Get the demorepo metadata, obtained from config.yml.")
    parser_info_subparsers = parser_info.add_subparsers(title='section', description='section to get information',
                                                        help='working mode to group commands based on it.',
                                                        dest='section')

    parser_info_demorepo = parser_info_subparsers.add_parser(
        'demorepo', description='Information about the demorepo.')
    parser_info_demorepo.add_argument('-v', '--version', action='store_true', help='Version of the demorepo.')

    parser_info_ci_tool = parser_info_subparsers.add_parser(
        'ci-tool', description='Information about the used ci-tool.')
    parser_info_ci_tool.add_argument('-n', '--name', action='store_true', help='ci-tool name.')
    parser_info_ci_tool.add_argument('-u', '--url', action='store_true', help='ci-tool url.')

    parser_info_projects = parser_info_subparsers.add_parser(
        'projects', description='Information about the projects.')
    parser_info_projects.add_argument('-p', '--path', action='store_true', help='Projects path.')
    # TODO: Implement this
    parser_info_projects.add_argument('-o', '--order', action='store_true',
                                      help='Dependency order of projects. Not specified projects have no dependencies.')


    parser_run_stage = subparsers.add_parser('run-stage',
                                       description='Run the stages for the target projects. If --targets and '
                                                   '--all-targets are not provided, it will check the differences from '
                                                   'last green commit (using the --ci-tool argument) and set them '
                                                   'as target projects.')

    parser_run_stage.add_argument('-p', '--path', required=True, help='Path to the projects folder.')
    parser_run_stage.add_argument('-s', '--stage', required=True, help='Stage name in the project demorepo.yml')
    parser_run_stage.add_argument('-e', '--env', action='append', help='Optional variables passed to the target stage script.'
                                                                 ' The format is VAR_NAME=VAR_VALUE. '
                                                                 'Multiple env vars can be specified.')
    parser_run_stage.add_argument('-r', '--recursive-deps', action='store_true',
                            help='Find projects recursively which depends on target projects and include them as '
                                 'target projects too.')
    parser_run_stage.add_argument('--ci-tool', default='gitlab', choices=['gitlab'],
                             help='The specific CI tool (e.g.: gitlab, Circle-CI, ....)')
    parser_run_stage.add_argument('--ci-url', help='the URL to the CI Server. By default uses the general public URL.')
    parser_run_stage.add_argument('-t', '--targets', help='A list of target project names to run the provided stage, '
                                                    'separated by blank spaces (use quotes around the string).')
    parser_run_stage.add_argument('--all-targets', action='store_true',
                            help='Set all the projects as target, and ignore --targets argument.')

    parser_run = subparsers.add_parser('run',
                                             description='Execute a shell command for the target projects. If --targets and '
                                                         '--all-targets are not provided, it will check the differences from '
                                                         'last green commit (using the --ci-tool argument) and set them '
                                                         'as target projects.')

    parser_run.add_argument('-p', '--path', required=True, help='Path to the projects folder.')
    parser_run.add_argument('-c', '--command', required=True, help='The shell command to execute.')
    parser_run.add_argument('-e', '--env', action='append',
                                  help='Optional variables passed to the target stage script.'
                                       ' The format is VAR_NAME=VAR_VALUE. '
                                       'Multiple env vars can be specified.')
    parser_run.add_argument('-r', '--recursive-deps', action='store_true',
                                  help='Find projects recursively which depends on target projects and include them as '
                                       'target projects too.')
    parser_run.add_argument('--ci-tool', default='gitlab', choices=['gitlab'],
                                  help='The specific CI tool (e.g.: gitlab, Circle-CI, ....)')
    parser_run.add_argument('--ci-url', help='the URL to the CI Server. By default uses the general public URL.')
    parser_run.add_argument('-t', '--targets', help='A list of target project names to run the provided stage, '
                                                          'separated by blank spaces (use quotes around the string).')
    parser_run.add_argument('--all-targets', action='store_true',
                                  help='Set all the projects as target, and ignore --targets argument.')



    parser_integration = subparsers.add_parser('integration')
    # TODO: Complete the integration part. Useful or treated as one more stage?

    args = vars(parser.parse_args())

    try:
        Repo(os.getcwd())
    except Exception as e:
        parser.error(f"ERROR: You must be in the root path of a git repository: {e}.")

    if args['working_mode'] == 'init':
        commands.init(args)
    if args['working_mode'] == 'info':
        commands.info(args)
    elif args['working_mode'] == 'run':
        commands.run(args)
    elif args['working_mode'] == 'run-stage':
        commands.run_stage(args)
    elif args['working_mode'] == 'integration':
        commands.integration(args)
    else:
        print(parser.parse_args('-h'))