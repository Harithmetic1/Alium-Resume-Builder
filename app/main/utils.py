'''Utility file for saving picture to a path'''
from flask import current_app as app
import os, secrets
from PIL import Image

def save_pic(picture, file_name=None):
    '''Helper function for saving an image object to the server'''
    picture = Image.open(picture)
    picture.thumbnail((150, 150))
    if not file_name:
        print(picture.filename)
        file_name = secrets.token_hex(8) + '.png' #os.path.splitext(picture.filename)[1]
        print(file_name)
        file_path = os.path.join(app.root_path, 'static/assets/user_images', file_name)
    picture.save(file_path)
    return file_name
