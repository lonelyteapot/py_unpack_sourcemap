import json
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any, TypeAlias, Union

from ._exceptions import PyUnpackSourcemapException
from ._logging import logger

AnyPath: TypeAlias = Union[Path, PathLike[str], str]


@dataclass
class Sourcemap:
    """Representation of a source map"""

    version: int
    sources: list[str]
    sources_content: list[str]

    def __post_init__(self):
        if self.version != 3:
            logger.warning(
                "Only source maps of version 3 are supported, "
                f"found version {self.version}"
            )
        if not self.sources:
            msg = "Source map doesn't contain any sources"
            raise PyUnpackSourcemapException(msg)
        if len(self.sources) != len(self.sources_content):
            msg = (
                "Number of sources and sourcesContent items do not match "
                f"({len(self.sources)} != {len(self.sources_content)})"
            )
            raise PyUnpackSourcemapException(msg)

    @classmethod
    def from_json(cls, data: dict[str, Any]):
        data = data.copy()
        version = data.pop("version")
        sources = data.pop("sources", [])
        sources_content = data.pop("sourcesContent", [])
        for unsupported_key in data:
            logger.warning('Unsupported key found in source map: "%s"', unsupported_key)
        return cls(
            version=version,
            sources=sources,
            sources_content=sources_content,
        )

    @classmethod
    def from_str(cls, data: str):
        return cls.from_json(json.loads(data))

    @classmethod
    def from_file(cls, path: AnyPath):
        path = Path(path)
        logger.info(f"Reading {path}")
        if not path.exists():
            msg = f"File {path} does not exist"
            raise PyUnpackSourcemapException(msg)
        if not path.is_file():
            msg = f"File {path} is not a file"
            raise PyUnpackSourcemapException(msg)
        data = path.read_text()
        return cls.from_str(data)

    def get_content_map(self) -> dict[str, str]:
        return dict(zip(self.sources, self.sources_content, strict=True))

    def extract_into_directory(self, output_dir: AnyPath, *, overwrite: bool = False):
        output_dir = Path(output_dir)
        logger.info(f"Extracting {len(self.sources)} sources into {output_dir}")
        if not output_dir.parent.exists():
            msg = f"Parent directory {output_dir.parent} does not exist"
            raise PyUnpackSourcemapException(msg)
        if not output_dir.parent.is_dir():
            msg = f"Parent {output_dir.parent} is not a directory"
            raise PyUnpackSourcemapException(msg)
        if not overwrite and output_dir.is_dir() and not _is_dir_empty(output_dir):
            msg = (
                f"Directory {output_dir} is not empty. "
                "Delete it or consider using overwrite=True"
            )
            raise PyUnpackSourcemapException(msg)
        for source_path, source_content in self.get_content_map():
            source_path = source_path.replace("://", "/")
            target_path = output_dir.joinpath(source_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(source_content)


def _is_dir_empty(path: Path):
    return next(path.iterdir(), None) is None
