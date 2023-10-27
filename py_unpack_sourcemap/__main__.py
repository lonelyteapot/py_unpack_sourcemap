"""
Module for command-line execution of py_unpack_sourcemap.
Usage: python -m py_unpack_sourcemap --help
"""

import argparse
import sys
from pathlib import Path

from ._exceptions import PyUnpackSourcemapException
from ._logging import configure_logging_for_cli, logger
from ._main import Sourcemap

DEFAULT_ERROR_RETCODE = 1


class CliArguments(argparse.Namespace):
    sourcemap: Path
    output_dir: Path
    overwrite: bool


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
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrite existing output directory",
    )
    return parser.parse_args(namespace=CliArguments())


def main_unsafe() -> None:
    parser = argparse.ArgumentParser()
    args = parse_arguments(parser)

    sourcemap = Sourcemap.from_file(args.sourcemap)
    sourcemap.extract_into_directory(args.output_dir, overwrite=args.overwrite)


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
