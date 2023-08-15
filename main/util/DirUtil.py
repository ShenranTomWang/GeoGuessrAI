import os

def get_root_dir() -> str:
    return os.getcwd()

def get_image_dir() -> str:
    return f'{get_root_dir()}/resources/streetview_images'

def get_model_dir() -> str:
    return f'{get_root_dir()}/resources/model_states'