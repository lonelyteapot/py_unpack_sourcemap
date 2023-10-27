from dataclasses import dataclass


@dataclass
# TODO: add subclasses
class PyUnpackSourcemapException(Exception):
    message: str
