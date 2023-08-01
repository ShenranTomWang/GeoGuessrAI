import os

def get_root_dir():
    return os.getcwd()

def get_image_dir():
    return f'{get_root_dir()}/resources/streetview_images'

def get_world_map_dir():
    return f'{get_root_dir()}/resources/streetview_downloader/WorldMap.geo.json'