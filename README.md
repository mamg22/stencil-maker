# stencil-maker

Generate an image as a text stencil, with custom fonts, sizes and optionally flipping the image horizontally.

## Installation

Get a instalable wheel from the [releases page](https://github.com/mamg22/stencil-maker/releases), once it downloads, install it with:

```console
$ pip install stencil_maker-VERSION-py3-none-any.whl
$ # The VERSION might be different depending on the version downloaded
```

To install with the server mode enabled, include the `[server]` extra feature when installing:

```console
$ pip install 'stencil_maker-VERSION-py3-none-any.whl[server]'
```

### From PyPI

Coming soon

## Usage

Whenever a font is required as an option, you may pass either a path pointing to the font or the font basename, which the library will try to find in the system's font directories.

### Command line

```console
$ # The -h or --help flags provide information on usage
$ stencil-maker --help
...
$ # Basic usage requires the font name or font filename and a output filename
$ # Provide the text to draw via stdin
$ stencil-maker -f LiberationSans-Regular output.png
My text may be split
into multiple lines
This is not a haiku
$ stencil-maker --font font-dir/LiberationSans-Bold.ttf --flip --size 300 output2.png
This is a test
$
```

### Server

This functionality will only be available if the package was installed with the `server` feature enabled.

The server program requires the `STENCIL_MAKER_FONT` environment variable to be defined, either in the program environment or a `.env` file.

To run the server you can quickly use the `stencil-server` command, which spins up a simple flask server running on `localhost` port `5000`. For futher customizing the server options, provide the path to the server module to your WSGI server and configure it to your liking. For example using `flask` as WSGI server and passing a few settings:

```console
flask run --port 5001 --host 0.0.0.0 --app stencil_maker.server
```

### Python library

This package provides a simple api to produce images. The main interface is the ```python stencil_maker.make_stencil()``` function, which returns a regular Pillow `Image` instance, which can be saved or processed further. For example:

```python
from stencil_maker import make_stencil

stencil = make_stencil("This is a test", "LiberationMono-Regular", 300)
stencil.save("my-stencil.png")
```
