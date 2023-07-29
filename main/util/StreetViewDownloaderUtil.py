import random
import google_streetview.api
import requests
import os
from . import StreetViewDownloaderConstants as constants
from . import DirUtil

# Function to generate random coordinates
def generate_coordinates() -> tuple:
    """Generates random coordinates
    """
    x = random.uniform(-90, 90)
    y = random.uniform(-180, 180)
    return (x, y)

def download_random_street_view_images(dataset_size=constants.DEFAULT_DATASET_SIZE, api_key=constants.API_KEY, image_size=constants.DEFAULT_IMAGE_SIZE) -> None:
    """
    Args:
        dataset_size (int, optional): size of dataset. Defaults to StreetViewDownloaderConstants.DEFAULT_DATASET_SIZE.
        api_key (string, optional): google street view api key. Defaults to StreetViewDownloaderConstants.API_KEY.
        image_size (string, optional): resolution of images in format (int)x(int). Defaults to StreetViewDownloaderConstants.DEFAULT_IMAGE_SIZE.
    """
    # Set up Google Street View API parameters
    params = {
        'size': image_size,  # Image size
        'fov': constants.DEFAULT_FOV,  # Field of view
        'key': api_key,
        'return_error_code': 'true'
    }

    # Create a directory to save the images
    images_dir = DirUtil.get_image_dir()
    os.makedirs(images_dir, exist_ok=True)
    
    coordinates = set()

    # Retrieve and save the images
    i = 0
    while i < dataset_size:
        coordinate = generate_coordinates()
        while coordinates.__contains__(coordinate):
            coordinate = generate_coordinates()
        params['location'] = f"{coordinate[0]},{coordinate[1]}"
        response = requests.get('https://maps.googleapis.com/maps/api/streetview', params=params)
        if response.status_code == 200:
            image_name = f"{images_dir}/{coordinate[0]}_{coordinate[1]}.jpg"
            with open(image_name, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded image {i+1} of 10000: {image_name}")
            i += 1

    print("All images downloaded successfully.")
