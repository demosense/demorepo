import argparse
import sys
import os
from git import Repo
from .commands import init, run, integration


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='demorepo',
                                     description='Tool to manage a monorepo, where projects can be general projects '
                                                 '(language code, build and test management...).')

    subparsers = parser.add_subparsers(title='working mode', description='init, run or integration',
                                       help='working mode to group commands based on it.',
                                       dest='command')

    parser_init = subparsers.add_parser('init',
                                        description="Select the CI tool and parameters to perform actions on demorepo.")
    parser_init.add_argument('--ci-tool', required=True, choices=['gitlab'],
                             help='The specific CI tool (e.g.: gitlab, Circle-CI, ...')
    parser_init.add_argument('-p', '--path', default='projects', help='Path to the projects folder.')
    parser_init.add_argument('--ci-url', default=None, help='The URL to the CI Server. '
                                                            'By default (None) uses the general public URL.')
    parser_init.add_argument('-r', '--recursive-deps', action='store_true',
                            help='Find projects recursively which depends on modified projects and include them as '
                                 'target projects.')

    parser_run = subparsers.add_parser('run',
                                       description='Run the stages for all the projects defined in each demorepo.yml')
    parser_run.add_argument('-s', '--stage', required=True, help='Stage name in the project demorepo.yml')
    parser_run.add_argument('-e', '--env', help='Optional variable passed to the target stage script.')
    parser_run.add_argument('-p', '--path', default='projects',
                            help='Path to the projects folder. If init command was executed before, it will use the '
                                 'same projects folder path by default.')
    parser_run.add_argument('-t', '--targets', default='ALL',
                            help='The target projects to run the stage. Can be ALL, or a list of project names '
                                 'separated by spaces (use quotes). If init command was executed before, it will use '
                                 'the computed target projects by default.')
    parser_init.add_argument('--all-targets', action='store_true',
                             help='Set all the projects as target, ignoring --targets argument.')


    parser_integration = subparsers.add_parser('integration')
    # TODO: Complete the integration part

    args = vars(parser.parse_args())

    print(args)

    try:
        Repo(os.getcwd())
    except:
        print("ERROR: You must be in the root path of a git repository.")
        sys.exit(-1)

    if args['command'] == 'init':
        init(args)
    elif args['command'] == 'run':
        run(args)
    elif args['command'] == 'integration':
        integration(args)
    else:
        print(parser.parse_args('-h'))