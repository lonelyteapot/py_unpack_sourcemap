from dataclasses import dataclass


# TODO: Add subclasses
@dataclass
class PyUnpackSourcemapException(Exception):
    message: str
