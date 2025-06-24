import argparse
from functools import partial
import sys

from stencil_maker import make_stencil

eprint = partial(print, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Simple tool to generte a stencil for text provided in stdin"
    )

    parser.add_argument("-f", "--font", required=True, help="Font to write text with")
    parser.add_argument(
        "-s", "--size", type=int, default=300, help="Font size in pixels"
    )
    parser.add_argument(
        "-F", "--flip", action="store_true", help="Flip final image horizontally"
    )
    parser.add_argument(
        "--fill",
        action="store_false",
        dest="stroked",
        help="Fill text instead of stroke",
    )
    parser.add_argument("--fill-color", help="Color to fill text with")
    parser.add_argument("--stroke-color", help="Color to draw the stroke with")
    parser.add_argument("--background-color", help="Image background color")
    parser.add_argument("filename", help="Filename to save the image to")

    args = parser.parse_args()

    text = sys.stdin.read().strip()

    if not text:
        eprint("No text provided")
        return

    try:
        image = make_stencil(
            text,
            args.font,
            args.size,
            flip=args.flip,
            stroked=args.stroked,
            fill_color=args.fill_color,
            stroke_color=args.stroke_color,
            background_color=args.background_color,
        )
    except OSError as err:
        eprint(f"Could not load font file '{args.font}': {err}")
        return

    try:
        image.save(args.filename, optimize=True, format="png")
    except (OSError, ValueError) as err:
        eprint(err)
        return


if __name__ == "__main__":
    main()
