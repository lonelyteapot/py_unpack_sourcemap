import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ._logging import logger


# TODO: add subclasses
@dataclass
class PyUnpackSourcemapException(Exception):
    message: str


@dataclass
class Sourcemap:
    version: int
    sources: list[str]
    sources_content: list[str]

    @classmethod
    def from_json(cls, data: dict[str, Any]):
        return cls(
            version=data.get("version", None),  # TODO: None does not belong here
            sources=data.get("sources", []),
            sources_content=data.get("sourcesContent", []),
        )


def validate_sourcemap(sourcemap: Sourcemap):
    if sourcemap.version != 3:
        logger.warning(
            "Only source maps of version 3 are supported, "
            f"found version {sourcemap.version}"
        )

    if not sourcemap.sources:
        errmsg = "No sources found in the sourcemap"
        raise PyUnpackSourcemapException(errmsg)

    if len(sourcemap.sources) != len(sourcemap.sources_content):
        errmsg = (
            "Number of sources and sourcesContent items do not match "
            f"({len(sourcemap.sources)} != {len(sourcemap.sources_content)})"
        )
        raise PyUnpackSourcemapException(errmsg)


def read_sourcemap_from_file(path: Path):
    logger.info(f"Reading {path}")

    # TODO: error handling
    content = path.read_text()
    data = json.loads(content)
    sourcemap = Sourcemap.from_json(data)
    return sourcemap


def write_source_contents_to_directory(sourcemap: Sourcemap, output_dir: Path):
    logger.info(f"Extracting {len(sourcemap.sources)} sources into {output_dir}")
    for source_path, source_content in zip(
        sourcemap.sources, sourcemap.sources_content, strict=True
    ):
        source_path = source_path.replace("://", "/")
        target_path = output_dir.joinpath(source_path)
        # TODO: error handling
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(source_content)
