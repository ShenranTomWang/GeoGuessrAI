import os

def get_root_dir():
    return os.path.split(os.path.split(os.getcwd())[0])[0]

def get_image_dir():
    return f'{get_root_dir()}/resources/streetview_images'