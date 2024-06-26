from PIL import Image, ImageDraw, ImageFont, ImageOps

def textbbox(text: str, font: ImageFont.FreeTypeFont, spacing: int) -> tuple[int, int, int, int]:
    tmp_draw = ImageDraw.ImageDraw(Image.new("1", (0, 0)))

    return tmp_draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)

def calculate_image_size(bbox: tuple[int, int, int, int], margin: int) -> tuple[int, int]:
    x0, y0, x1, y1 = bbox
    
    return (abs(x1 - x0) + margin * 2, abs(y1 - y0) + margin * 2)

def draw_base_image(text: str, font_filename: str, font_size: int) -> Image.Image:
    font = ImageFont.truetype(font_filename, size=font_size)
    full_height = sum(abs(val) for val in font.getmetrics())
    margin = full_height // 5
    spacing = full_height // 5

    bbox = textbbox(text, font, spacing)

    img_size = calculate_image_size(bbox, margin)

    image = Image.new("L", img_size, color="white")
    draw = ImageDraw.ImageDraw(image)

    x0, y0, *_ = bbox

    x_offset = margin - x0
    y_offset = margin - y0

    draw.multiline_text((x_offset, y_offset), text, font=font, fill="black", spacing=spacing)

    return image


def make_stencil(text: str, font_filename: str, font_size: int, flip: bool = False) -> Image.Image:
    image = draw_base_image(text, font_filename, font_size)

    if flip:
        image = ImageOps.mirror(image)

    return image