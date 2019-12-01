import random as rnd

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter


def generate(text, font, text_color, font_size, orientation, space_width, character_spacing, fit):
    if orientation == 0:
        return _generate_horizontal_text(
            text, font, text_color, font_size, space_width, character_spacing, fit
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text, font, text_color, font_size, space_width, character_spacing, fit
        )
    else:
        raise ValueError("Unknown orientation " + str(orientation))


def _generate_horizontal_text(text, font, text_color, font_size, space_width, character_spacing, fit):
    text_width = 0
    text_height = 0
    lines = text.splitlines()
    image_font = ImageFont.truetype(font=font, size=font_size)
    space_width = int(image_font.getsize(" ")[0] * space_width)

    char_widths_by_line_number = {}
    for index, line in enumerate(lines):
        if not line:
            continue

        char_widths = [
            image_font.getsize(c)[0] if c != " " else space_width for c in line
        ]

        char_widths_by_line_number[index] = char_widths
        text_width = max(text_width, sum(char_widths) + character_spacing * (len(line) - 1))
        text_height = max(text_height, max([image_font.getsize(c)[1] for c in line]))

    txt_img = Image.new("RGBA", (text_width, len(lines) * (text_height + 5)), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )

    line_y_start = 0
    for line_number, line in enumerate(lines):
        if line:
            for i, c in enumerate(line):
                char_widths = char_widths_by_line_number[line_number]
                txt_draw.text(
                    (sum(char_widths[0:i]) + i * character_spacing, line_y_start),
                    c,
                    fill=fill,
                    font=image_font,
                )

            line_y_start += text_height

    if fit:
        return txt_img.crop(txt_img.getbbox())
    else:
        txt_img.save('raw.png')
        return txt_img


def _generate_vertical_text(text, font, text_color, font_size, space_width, character_spacing, fit):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(" ")[1] * space_width)

    char_heights = [
        image_font.getsize(c)[1] if c != " " else space_height for c in text
    ]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights) + character_spacing * len(text)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
    )

    for i, c in enumerate(text):
        txt_draw.text((0, sum(char_heights[0:i]) + i * character_spacing), c, fill=fill, font=image_font)

    if fit:
        return txt_img.crop(txt_img.getbbox())
    else:
        return txt_img
