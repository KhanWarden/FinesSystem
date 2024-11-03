from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

project_folder = Path(__file__).parent.parent.parent.parent
images_folder = project_folder / 'app' / 'certificates' / 'src'
font_path = project_folder / 'app' / 'certificates' / 'fonts' / 'MyriadPro-Regular.otf'
font_for_5k = ImageFont.truetype(font_path, 30)
font_for_10k = ImageFont.truetype(font_path, 45)
color = (0, 0, 0)

output_path_for_5k = project_folder / 'app' / 'certificates' / 'output' / "cert_5k_output.jpg"
output_path_for_10k = project_folder / 'app' / 'certificates' / 'output' / "cert_10k_output.jpg"


def draw_5k(date_of_cert, number):
    image_5k = Image.open(images_folder / 'cert_5k.jpg')
    draw = ImageDraw.Draw(image_5k)
    date_of_cert = datetime.strptime(date_of_cert, '%Y-%m-%d')

    # DATE
    date_text = date_of_cert.strftime('%d.%m.%Y')
    draw.text((625, 985), date_text, fill=color, font=font_for_5k)

    # NUMBER
    number_text = f"ONLINE - {number}"
    draw.text((900, 985), number_text, fill=color, font=font_for_5k)

    image_5k.save(output_path_for_5k)
    return output_path_for_5k


def draw_10k(date_of_cert, number):
    image_10k = Image.open(images_folder / 'cert_10k.jpg')
    draw = ImageDraw.Draw(image_10k)
    date_of_cert = datetime.strptime(date_of_cert, '%Y-%m-%d')

    # DATE
    date_text = date_of_cert.strftime('%d.%m.%Y')
    draw.text((610, 2150), date_text, fill=color, font=font_for_10k)

    # NUMBER
    number_text = f"ONLINE - {number}"
    draw.text((900, 2150), number_text, fill=color, font=font_for_10k)

    image_10k.save(output_path_for_10k)
    return output_path_for_10k
