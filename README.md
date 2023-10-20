# py_unpack_sourcemap

Unpack JavaScript source maps into source files

[![PyPI - Version](https://img.shields.io/pypi/v/py_unpack_sourcemap)][PyPI]
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py_unpack_sourcemap)][PyPI]
[![PyPI - Status](https://img.shields.io/pypi/status/py_unpack_sourcemap)][PyPI]
[![License](https://img.shields.io/github/license/lonelyteapot/py_unpack_sourcemap)][GitHub]


## Description

This Python tool allows you to unpack JavaScript source maps into their
corresponding source files. It can be particularly useful for debugging and
analyzing minified JavaScript code in production environments.

Modern browsers like Chrome and Firefox provide this functionality in DevTools.
However, they only let you view the source code in the browser itself, which can
be limiting. This tool allows you to extract the whole source tree for viewing
it in your favourite IDE.

## Installation

Ensure you have Python 3.10 or later installed.
The package is not tested on older versions, but they will probably work.

You can install the tool from [PyPI] using pip:

```sh
pip install py_unpack_sourcemap
```

Or [Poetry]:

```sh
poetry add py_unpack_sourcemap
```


## Usage

### As a command-line tool

```
python -m py_unpack_sourcemap [-h] -o OUTPUT_DIR sourcemap

positional arguments:
  sourcemap             path to the source map (a .js.map file)

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        a directory to extract source files into
```

### As a Python module

> No information here yet :( Use autocompletion or view the source code.

## Contributing

Any contributions are appreciated. Regular stuff.
Don't be afraid to create issues for any features you need.

## Contributors

- [lonelyteapot](https://github.com/lonelyteapot) - Original author

## License

This project is licensed under the [MIT License](https://mit-license.org/).


[GitHub]: https://github.com/lonelyteapot/py_unpack_sourcemap
[PyPI]: https://pypi.org/project/py_unpack_sourcemap/
[Poetry]: https://python-poetry.org/
