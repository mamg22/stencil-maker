from io import BytesIO
import os
import sys

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

from stencil_maker import make_stencil

load_dotenv()

app = Flask(__name__)

try:
    FONT: str = os.path.expanduser(os.environ["STENCIL_MAKER_FONT"])
except KeyError:
    print(
        "Font is not defined, set STENCIL_MAKER_FONT to the font file or font name to use",
        file=sys.stderr,
    )


@app.route("/")
def index():
    return render_template("index.html")


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

    flip = request.args.get("flip") == "on"
    stroked = not request.args.get("fill") == "on"
    size = request.args.get("fontsize", 300, type=int)
    image_format = request.args.get("format", "png")
    download = request.args.get("download") == "true"

    if size not in range(1, 500 + 1):
        return f"Invalid font size '{size}'", 400
    if image_format not in {"png", "jpeg"}:
        return f"Unsupported image format '{image_format}'", 400

    stencil = make_stencil(
        text,
        FONT,
        size,
        flip=flip,
        stroked=stroked,
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
