# 5879281275:AAEJINs_K7ZPIrsZBV9uF6timz8EGrdeV9I


import requests
import os
import time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

TOKEN = '5879281275:AAEJINs_K7ZPIrsZBV9uF6timz8EGrdeV9I'


def generate_image(text):
    # Define image parameters
    img_width = 1024
    img_height = 512
    font_size = 50
    font_color = (255, 255, 255)
    bg_color = (0, 0, 0)

    # Create image object
    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Define font and text parameters
    font_path = 'arial.ttf'
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate text position
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2

    # Draw text on image
    draw.text((x, y), text, fill=font_color, font=font)

    # Save image to buffer
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer


def send_image(chat_id, image):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    files = {'photo': ('image.png', image)}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response


def handle_message(message):
    chat_id = message['chat']['id']
    text = message['text']

    image = generate_image(text)
    send_image(chat_id, image)


def get_updates():
    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    response = requests.get(url)
    return response.json()


def main():
    last_update_id = None
    while True:
        updates = get_updates()['result']
        if updates:
            for update in updates:
                if last_update_id is None or update['update_id'] > last_update_id:
                    last_update_id = update['update_id']
                    if 'message' in update and 'text' in update['message']:
                        handle_message(update['message'])
        time.sleep(1)


if __name__ == '__main__':
    main()
