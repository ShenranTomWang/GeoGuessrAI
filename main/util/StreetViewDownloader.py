import random
import streetview
from geopy.geocoders import Nominatim
import os
from . import StreetViewDownloaderConstants as constants
from . import DirUtil

class StreetViewDownloader:
    
    def __init__(self, dataset_size=constants.DEFAULT_DATASET_SIZE, api_key=constants.API_KEY, image_size=constants.DEFAULT_IMAGE_SIZE, fov=constants.DEFAULT_FOV) -> None:
        """
        Args:
            dataset_size (int, optional): size of dataset. Defaults to constants.DEFAULT_DATASET_SIZE.
            api_key (string, optional): google street view static api key. Defaults to constants.API_KEY.
            image_size (string, optional): image size in format <int>x<int>, max 640x640. Defaults to constants.DEFAULT_IMAGE_SIZE.
            fov (string, optional): image field of view. Defaults to constants.DEFAULT_FOV.
        """
        self.geolocator = Nominatim(user_agent='StreetViewDownloader')
        self.dataset_size = dataset_size
        self.api_key = api_key
        self.image_size = image_size
        self.fov = fov

    def generate_coordinates(self) -> tuple:
        """Generates random coordinates
        """
        x = random.uniform(-90, 90)
        y = random.uniform(-180, 180)
        return (x, y)

    def download_random_street_view_images(self) -> None:
        """Generates random street view images
        """
        # Generate coordinates
        coordinates = []
        pano_ids = []
        i = 1
        while coordinates.__len__() < self.dataset_size:
            print(f'Attempt to generate coordinates {i}')
            coordinate = self.generate_coordinates()
            if self.check_coordinates_on_land(coordinate):
                print('Coordinates are on land')
                pano = self.check_coordinates_have_panorama(coordinate)
                if (pano != False):
                    print('Coordinates have panorama')
                    coordinates.append(coordinate)
                    pano_ids.append(pano.pano_id)
            i += 1
                    
        
        # Set up Google Street View API parameters
        # params = {
        #     'size': self.image_size,  # Image size
        #     'fov': self.fov,  # Field of view
        #     'key': self.api_key,
        #     'return_error_code': 'true'
        # }

        # Create a directory to save the images
        images_dir = DirUtil.get_image_dir()
        os.makedirs(images_dir, exist_ok=True)

        # Retrieve and save the images
        i = 0
        while i < self.dataset_size:
            coordinate = coordinates[i]
            pano_id = pano_ids[i]
            image = streetview.get_panorama(pano_id=pano_id)
            image_name = f"{images_dir}/{coordinate[0]}_{coordinate[1]}.jpg"
            image.save(image_name, "jpeg")
            # params['location'] = f"{coordinate[0]},{coordinate[1]}"
            # response = requests.get(constants.STREETVIEW_API_BASE_URL, params=params)
            # if response.status_code == 200:
            #     image_name = f"{images_dir}/{coordinate[0]}_{coordinate[1]}.jpg"
            #     with open(image_name, 'wb') as f:
            #         f.write(response.content)
            #     print(f"Downloaded image {i+1} of 10000: {image_name}")
            i += 1

        print("All images downloaded successfully.")

    def check_coordinates_have_panorama(self, coordinate) -> streetview.search.Panorama | bool:
        """Check whether the given coordinates have a panorama

        Args:
            coordinate (tuple<float, float>): coordinates <lat, lon>

        Returns:
            streetview.search.Panorama | bool: returns the panorama metadata if it exists, False otherwise
        """
        panos = streetview.search_panoramas(coordinate[0], coordinate[1])
        if panos.__len__() == 0:
            return False
        return panos[0]

    def check_coordinates_on_land(self, coordinate) -> bool:
        """Check whether the given coordinates are on land

        Args:
            coordinate (tuple<float, float>): coordinates <lat, lon>

        Returns:
            bool: whether the given coordinates are on land
        """
        location = self.geolocator.reverse(f'{coordinate[0]}, {coordinate[1]}')
        return location != None