from collections.abc import Iterable
from io import BytesIO
import itertools
import os
from pathlib import Path
import sys

try:
    from flask import (
        Flask,
        Blueprint,
        render_template,
        request,
        send_file,
        make_response,
        url_for,
    )
    from dotenv import load_dotenv
except ModuleNotFoundError as err:
    err.add_note(
        "Could not load required dependency, try installing this package with the [server] extra enabled"
    )
    raise

from stencil_maker import make_stencil

load_dotenv()

app = Flask(__name__)


def load_fonts() -> Iterable[Path]:
    font_directories = [
        Path(p)
        for p in (
            "/usr/share/fonts/",
            "/usr/local/share/fonts/",
            "~/.local/share/fonts/",
            ".",
        )
    ]

    font_files = itertools.chain.from_iterable(
        d.rglob("*.[ot]tf") for d in font_directories
    )

    return font_files


@app.route("/")
def index():
    return render_template("index.html", font_files=load_fonts())


@app.route("/fragments/result")
def result():
    response = make_response(render_template("result-fragment.html"))

    response.headers.add("HX-Replace-Url", url_for("index", **request.args.to_dict()))  # pyright:ignore

    return response


api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@api_v1.route("stencil")
def generate_stencil():
    text = request.args.get("text")

    if text is None:
        return "No text provided", 400

    text = text.replace("\r\n", "\n")

    font = request.args.get("font")
    flip = request.args.get("flip") == "on"
    stroked = not request.args.get("fill") == "on"
    size = request.args.get("fontsize", 300, type=int)
    image_format = request.args.get("format", "png")
    fill_color = request.args.get("fill_color", "#FFFFFF")
    stroke_color = request.args.get("stroke_color", "#FFFFFF")
    background_color = request.args.get("background_color", "#FFFFFF")
    download = request.args.get("download") == "true"

    if size not in range(1, 500 + 1):
        return f"Invalid font size '{size}'", 400
    if image_format not in {"png", "jpeg"}:
        return f"Unsupported image format '{image_format}'", 400
    if not font:
        return f"Invalid font `{font}`", 400

    stencil = make_stencil(
        text,
        font,
        size,
        flip=flip,
        stroked=stroked,
        fill_color=fill_color,
        stroke_color=stroke_color,
        background_color=background_color,
    )

    bio = BytesIO()
    stencil.save(bio, image_format)
    bio.seek(0)

    return send_file(
        bio, f"image/{image_format}", as_attachment=download, download_name="stencil"
    )


app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run()
