import sys

from templator.commands import create_parser, process_command


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    process_command(args)


if __name__ == "__main__":
    main()
