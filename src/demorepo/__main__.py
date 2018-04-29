
from demorepo import parser
from demorepo import commands


__package__ = "demorepo"


def main():
    args = parser.parse_args()
    commands.exec_command(args)


if __name__ == '__main__':
    main()
