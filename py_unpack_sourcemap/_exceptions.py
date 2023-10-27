# TODO: Add subclasses


class PyUnpackSourcemapException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class SourcemapParsingException(PyUnpackSourcemapException):
    pass
