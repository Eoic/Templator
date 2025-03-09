import argparse
from typing import TYPE_CHECKING, Any

from templator.compiler import compile

if TYPE_CHECKING:
    _SubparserType = argparse._SubParsersAction[argparse.ArgumentParser]
else:
    _SubparserType = Any


def add_compile_parser(subparsers: _SubparserType):
    parser = subparsers.add_parser(
        "compile",
        help="Compile templates.",
        usage="%(prog)s [compile]",
    )

    parser.add_argument(
        "-i",
        "--input-dir",
        help="Input directory where the template files are stored.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        help="Output directory where the compiled HTML files should be stored.",
        default="dist",
        type=str,
    )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="templator",
        description="A simple static site generator.",
    )

    subparsers = parser.add_subparsers(dest="command")
    add_compile_parser(subparsers)

    return parser


def process_command(args: argparse.Namespace):
    match args.command:
        case "compile":
            compile(args.input_dir, args.output_dir)
