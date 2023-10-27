# py_unpack_sourcemap

Unpack JavaScript source maps into source files

[![PyPI - Version](https://img.shields.io/pypi/v/py_unpack_sourcemap)][PyPI]
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py_unpack_sourcemap)][PyPI]
[![PyPI - Status](https://img.shields.io/pypi/status/py_unpack_sourcemap)][PyPI]
[![License](https://img.shields.io/github/license/lonelyteapot/py_unpack_sourcemap)][GitHub]

## Description

This Python tool allows you to extract JavaScript source files from source maps.
It can be particularly useful for debugging and analyzing minified JavaScript
code in production environments.

Modern browsers like Chrome and Firefox provide this functionality in DevTools.
However, they only let you view the source code in the browser itself, which can
be limiting. This tool allows you to extract the whole source tree for viewing
it in your favourite IDE.

This projects aims to follow the
[Source Map Revision 3 Proposal](https://sourcemaps.info/spec.html).
Only the `sourcesContent` field is currently supported.
See [Roadmap](#roadmap) for what is lacking.

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
python -m py_unpack_sourcemap [-h] -o OUTPUT_DIR [--overwrite] sourcemap

positional arguments:
  sourcemap             path to the source map (a .js.map file)

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        a directory to extract source files into
  --overwrite           overwrite existing output directory
```

### As a Python module

> No information here yet :( Use autocompletion or view the source code.

## Roadmap

This project is developed on demand.
If you need a feature, [submit an issue][new issue] to express your interest.

- [ ] Support for fetching remote source maps via HTTP
- [ ] Support for `null` elements in `sourcesContent` field
- [ ] More tests
- [ ] Support for `sourceRoot` field
- [ ] Support for `names` field
- [ ] Support for `mappings` field
- [ ] "Index map" format (`sections` field)
- [ ] GitHub workflows for tests and publishing

[//]: # "when editing, please remove entries instead of checking them off"

## Contributing

Any contributions are appreciated. Regular stuff.
Don't be afraid to submit issues or PRs.

## Contributors

- [lonelyteapot](https://github.com/lonelyteapot) - original author

## License

This project is licensed under the [MIT License](https://mit-license.org/).

[GitHub]: https://github.com/lonelyteapot/py_unpack_sourcemap
[new issue]: https://github.com/lonelyteapot/py_unpack_sourcemap/issues/new
[PyPI]: https://pypi.org/project/py_unpack_sourcemap/
[Poetry]: https://python-poetry.org/
