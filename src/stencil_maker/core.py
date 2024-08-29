from typing import NamedTuple, Self

from PIL import Image, ImageDraw, ImageFont, ImageOps

dummy_draw = ImageDraw.ImageDraw(Image.new("1", (0, 0)))

type Color = float | tuple[int, ...] | str


class BoundingBox(NamedTuple):
    x0: int
    y0: int
    x1: int
    y1: int

    def transformed(
        self, move_x: int = 0, move_y: int = 0, resize_x: int = 0, resize_y: int = 0
    ) -> Self:
        return self.__class__(
            self.x0 + move_x,
            self.y0 + move_y,
            self.x1 + move_x + resize_x,
            self.y1 + move_y + resize_y,
        )

    @property
    def width(self) -> int:
        return abs(self.x1 - self.x0)

    @property
    def height(self) -> int:
        return abs(self.y1 - self.y0)


def calculate_image_size(bbox: BoundingBox, margin: int) -> tuple[int, int]:
    return (bbox.width + margin * 2, bbox.height + margin * 2)


def draw_base_image(
    text: str,
    font_filename: str,
    font_size: int,
    stroke_width: int = 0,
    background_color: Color = "white",
    fill_color: Color = "black",
    stroke_color: Color = "black",
) -> Image.Image:
    font = ImageFont.truetype(font_filename, size=font_size)
    ascent, descent = (abs(val) for val in font.getmetrics())
    full_height = ascent + descent

    margin = max(abs(full_height // 10), 1)
    spacing = margin

    boxes: list[tuple[str, BoundingBox]] = []

    for line in text.splitlines():
        bbox = dummy_draw.textbbox(
            (0, 0), line, font, stroke_width=stroke_width, anchor="lt"
        )
        bounding = BoundingBox(*bbox)
        boxes.append((line, bounding))

    x0 = min(box.x0 for _, box in boxes)
    y0 = min(box.y0 for _, box in boxes)
    x1 = max(box.x1 for _, box in boxes)
    y1 = sum(box.height for _, box in boxes) + spacing * (len(boxes) - 1)

    bbox = BoundingBox(x0, y0, x1, y1).transformed(margin, margin)

    img_size = calculate_image_size(bbox, margin)

    image = Image.new("L", img_size, color=background_color)
    draw = ImageDraw.ImageDraw(image)

    offset = margin
    for text, box in boxes:
        adjbox = box.transformed(margin - box.x0, offset - box.y0)

        draw.text(
            adjbox.transformed(-box.x0, -box.y0)[:2],
            text,
            font=font,
            fill=fill_color,
            spacing=spacing,
            stroke_width=stroke_width,
            stroke_fill=stroke_color,
            anchor="lt",
        )

        offset += box.height + spacing

    return image


def make_stencil(
    text: str,
    font_filename: str,
    font_size: int,
    flip: bool = False,
    stroked: bool = True,
) -> Image.Image:
    if stroked:
        fill = "white"
        stroke_width = max(font_size // 50, 1)
        stroke_color = "black"
    else:
        fill = "black"
        stroke_width = 0
        stroke_color = "white"

    image = draw_base_image(
        text,
        font_filename,
        font_size,
        stroke_width=stroke_width,
        fill_color=fill,
        stroke_color=stroke_color,
    )

    if flip:
        image = ImageOps.mirror(image)

    return image
