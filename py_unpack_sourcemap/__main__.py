"""
Module for command-line execution of py_unpack_sourcemap.
Usage: python -m py_unpack_sourcemap --help
"""

import argparse
import sys
from pathlib import Path

from ._logging import configure_logging_for_cli, logger
from ._main import (
    PyUnpackSourcemapException,
    read_sourcemap_from_file,
    validate_sourcemap,
    write_source_contents_to_directory,
)

DEFAULT_ERROR_RETCODE = 1


class CliArguments(argparse.Namespace):
    sourcemap: Path
    output_dir: Path


def parse_arguments(parser: argparse.ArgumentParser) -> CliArguments:
    parser.prog = "py_unpack_sourcemap"
    parser.description = "Unpack JavaScript source maps into source files"
    parser.add_argument(
        "sourcemap",
        type=Path,
        help="path to the source map (a .js.map file)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        type=Path,
        help="a directory to extract source files into",
    )
    return parser.parse_args(namespace=CliArguments())


def validate_arguments(args: CliArguments) -> None:
    if not args.sourcemap.is_file():
        errmsg = f"{args.sourcemap} is not a file, expected path to a source map"
        raise PyUnpackSourcemapException(errmsg)

    if args.output_dir.exists():
        if not args.output_dir.is_dir():
            errmsg = f"{args.output_dir} is not a directory, expected a clean directory"
            raise PyUnpackSourcemapException(errmsg)
        has_files = any(True for _ in args.output_dir.iterdir())
        if has_files:
            errmsg = f"{args.output_dir} is not empty, expected a clean directory"
            raise PyUnpackSourcemapException(errmsg)


def main_unsafe() -> None:
    parser = argparse.ArgumentParser()
    args = parse_arguments(parser)
    validate_arguments(args)

    sourcemap = read_sourcemap_from_file(args.sourcemap)
    validate_sourcemap(sourcemap)

    write_source_contents_to_directory(sourcemap, args.output_dir)


def main() -> None:
    configure_logging_for_cli()

    try:
        main_unsafe()
    except PyUnpackSourcemapException as e:
        logger.error(f"{e.message}")
        sys.exit(DEFAULT_ERROR_RETCODE)

    logger.info("Done!")


if __name__ == "__main__":
    main()
