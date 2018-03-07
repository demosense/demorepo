import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='demorepo',
                                     description='Tool to manage a monorepo, where projects can be general projects '
                                                 '(code language, build and test management...).')

    subparsers = parser.add_subparsers(title='working mode', description='init, run or integration',
                                       help='working mode to group commands based on it')

    parser_init = subparsers.add_parser('init')
    parser_init.add_argument('--ci-tool', required=True, help='The specific CI tool (e.g.: gitlab, Circle-CI, ...')
    parser_init.add_argument('-R', '--recursive-deps', action='store_true',
                             help='Find projects recursively which depends on modified projects and include them as '
                                  'target projects.')

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('-s', '--stage', required=True, help='Stage name in the project demorepo.yml')
    parser_run.add_argument('-e', '--env', help='Optional variable passed to the target stage script')

    parser_integration = subparsers.add_parser('integration')

    args = parser.parse_args(['integration', '-h'])
