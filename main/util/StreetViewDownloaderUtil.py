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

def download_random_street_view_images(dataset_size=constants.DEFAULT_DATASET_SIZE, api_key=constants.API_KEY, image_size=constants.DEFAULT_IMAGE_SIZE):
    """
    Args:
        dataset_size (int, optional): size of dataset. Defaults to StreetViewDownloaderConstants.DEFAULT_DATASET_SIZE.
        api_key (string, optional): google street view api key. Defaults to StreetViewDownloaderConstants.API_KEY.
        image_size (string, optional): resolution of images in format (int)x(int). Defaults to StreetViewDownloaderConstants.DEFAULT_IMAGE_SIZE.
    """
    # Generate random coordinates
    coordinates = []
    while len(coordinates) < dataset_size:
        coordinate = generate_coordinates()
        if check_street_view_availability(api_key, coordinate):
            coordinates.append(coordinate)

    # Set up Google Street View API parameters
    params = {
        'size': image_size,  # Image size
        'fov': '90',  # Field of view
        'pitch': '0',  # Camera pitch angle
        'key': api_key
    }

    # Create a directory to save the images
    images_dir = DirUtil.get_image_dir()
    os.makedirs(images_dir, exist_ok=True)

    # Retrieve and save the images
    for i, coordinate in enumerate(coordinates):
        params['location'] = f"{coordinate[0]},{coordinate[1]}"
        results = google_streetview.api.results(params)
        image_name = f"{images_dir}/{coordinate[0]}_{coordinate[1]}.jpg"
        results.download_links(image_name)
        print(f"Downloaded image {i+1} of 10000: {image_name}")

    print("All images downloaded successfully.")

def check_street_view_availability(api_key, coordinate) -> bool:
    """Check if street view is available at coordinate

    Args:
        api_key (string): Google Street View API key
        coordinate (tuple(int, int)): coordinate to check
    """
    params = {
            'location': f"{coordinate[0]},{coordinate[1]}",
            'key': api_key
        }
    metadata = requests.get('https://maps.googleapis.com/maps/api/streetview/metadata', params=params)
    return metadata.status_code == 200
