import os

def get_root_dir() -> str:
    return os.getcwd()

def get_training_image_dir() -> str:
    return f'{get_root_dir()}/resources/streetview_images_train'

def get_testing_image_dir() -> str:
    return f'{get_root_dir()}/resources/streetview_images_test'

def get_model_dir() -> str:
    return f'{get_root_dir()}/resources/model_states'