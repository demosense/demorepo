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
                                       dest='command')

    parser_init = subparsers.add_parser('init', description="Register a git repository in demorepo package.")
    # TODO: Complete the init part. Useful?

    parser_run = subparsers.add_parser('run',
                                       description='Run the stages for the target projects. If --targets and '
                                                   '--all-targets are not provided, it will check the differences from '
                                                   'last green commit (using the --ci-tool argument) and set them '
                                                   'as target projects.')

    parser_run.add_argument('-p', '--path', required=True, help='Path to the projects folder.')
    parser_run.add_argument('-s', '--stage', required=True, help='Stage name in the project demorepo.yml')
    parser_run.add_argument('-e', '--env', help='Optional variable passed to the target stage script.')
    parser_run.add_argument('-r', '--recursive-deps', action='store_true',
                            help='Find projects recursively which depends on target projects and include them as '
                                 'target projects too.')
    parser_run.add_argument('--ci-tool', default='gitlab', choices=['gitlab'],
                             help='The specific CI tool (e.g.: gitlab, Circle-CI, ...')
    parser_run.add_argument('--ci-url', help='the URL to the CI Server. By default uses the general public URL.')
    parser_run.add_argument('-t', '--targets', help='A list of target project names to run the provided stage, '
                                                    'separated by blank spaces (use quotes around the string).')
    parser_run.add_argument('--all-targets', action='store_true',
                            help='Set all the projects as target, and ignore --targets argument.')

    parser_integration = subparsers.add_parser('integration')
    # TODO: Complete the integration part. Useful or treated as one more stage?

    args = vars(parser.parse_args())
    print(args)

    try:
        Repo(os.getcwd())
    except:
        parser.error("ERROR: You must be in the root path of a git repository.")

    if args['command'] == 'init':
        commands.init(args)
    elif args['command'] == 'run':
        commands.run(args)
    elif args['command'] == 'integration':
        commands.integration(args)
    else:
        print(parser.parse_args('-h'))