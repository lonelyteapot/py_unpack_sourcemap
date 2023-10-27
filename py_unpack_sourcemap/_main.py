import json
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any, Optional, TypeAlias, Union

from ._exceptions import PyUnpackSourcemapException, SourcemapParsingException
from ._logging import logger

AnyPath: TypeAlias = Union[Path, PathLike[str], str]


@dataclass
class Sourcemap:
    """Representation of a source map"""

    version: int
    file: Optional[str]
    sourceRoot: Optional[str]
    sources: list[str]
    sourcesContent: Optional[list[str]]
    names: list[str]
    mappings: str

    def __post_init__(self):
        if self.version != 3:
            logger.warning(f"Unsupported source map version ({self.version})")
        if not self.sources:
            msg = "Source map does not contain any sources"
            raise PyUnpackSourcemapException(msg)
        if self.sourcesContent and len(self.sources) != len(self.sourcesContent):
            msg = (
                "Number of sources and sourcesContent items do not match "
                f"({len(self.sources)} != {len(self.sourcesContent)})"
            )
            raise PyUnpackSourcemapException(msg)

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        data = data.copy()

        version = data.pop("version", None)
        file = data.pop("file", None)
        sourceRoot = data.pop("sourceRoot", None)
        sources = data.pop("sources", None)
        sourcesContent = data.pop("sourcesContent", None)
        names = data.pop("names", None)
        mappings = data.pop("mappings", None)

        missing_fields = []
        if version is None:
            missing_fields.append("version")
        if sources is None:
            missing_fields.append("sources")
        if names is None:
            missing_fields.append("names")
        if mappings is None:
            missing_fields.append("mappings")
        if missing_fields:
            msg = f"Source map is missing required fields: {missing_fields}"
            raise SourcemapParsingException(msg)

        result = cls(
            version=version,
            file=file,
            sourceRoot=sourceRoot,
            sources=sources,
            sourcesContent=sourcesContent,
            names=names,
            mappings=mappings,
        )

        for unsupported_key, value in data:
            logger.warning('Unsupported key found in source map: "%s"', unsupported_key)
            setattr(result, unsupported_key, value)

        return result

    @classmethod
    def from_json_str(cls, data: str):
        obj = json.loads(data)
        if not isinstance(obj, dict):
            msg = "Expected a single JSON object"
            raise SourcemapParsingException(msg)
        return cls.from_dict(obj)

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
        data = path.read_text(encoding="utf-8")
        return cls.from_json_str(data)

    def get_content_map(self) -> dict[str, str]:
        if not self.sourcesContent:
            msg = "Source maps without the 'sourcesContent' field are not supported"
            raise PyUnpackSourcemapException(msg)
        if any(content is None for content in self.sourcesContent):
            msg = (
                "Source maps with 'null' elements in 'sourcesContent' are not supported"
            )
        return dict(zip(self.sources, self.sourcesContent, strict=True))

    def extract_into_directory(
        self,
        output_dir: AnyPath,
        *,
        overwrite: bool = False,
        ignore_source_root: bool = False,
    ):
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

        source_root = "."
        if not ignore_source_root and self.sourceRoot:
            # TODO: Handle absolute and relative source roots differently
            source_root = self.sourceRoot.removeprefix("/")

        for source_path, source_content in self.get_content_map().items():
            source_path = source_path.replace("://", "/")
            target_path = output_dir.joinpath(source_root, source_path).resolve()
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(source_content, encoding="utf-8")


def _is_dir_empty(path: Path):
    return next(path.iterdir(), None) is None
