from PIL import Image, ImageDraw, ImageFont, ImageOps

def calculate_image_size(text: str, font: ImageFont.FreeTypeFont, margin: int) -> tuple[int, int]:
    tmp_draw = ImageDraw.ImageDraw(Image.new("1", (0, 0)))

    bounding_box = tmp_draw.multiline_textbbox((0, 0), text, font=font)
    return (margin*2 + bounding_box[2], margin*2 + bounding_box[3])

def draw_base_image(text: str, font_filename: str, font_size: int) -> Image.Image:
    margin = round(font_size / 10)
    font = ImageFont.truetype(font_filename, size=font_size)

    img_size = calculate_image_size(text, font, margin)

    image = Image.new("L", img_size, color="white")
    draw = ImageDraw.ImageDraw(image)

    draw.multiline_text((margin, 0), text, font=font, fill="black")

    return image


def make_stencil(text: str, font_filename: str, font_size: int, flip: bool = False) -> Image.Image:
    image = draw_base_image(text, font_filename, font_size)

    if flip:
        image = ImageOps.mirror(image)

    return image