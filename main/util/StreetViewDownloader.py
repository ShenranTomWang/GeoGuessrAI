import streetview
from geopy.geocoders import Nominatim
import os
import json
import requests
from . import StreetViewDownloaderConstants as constants
from . import DirUtil

class StreetViewDownloader:
    """Class that abstracts a downloader of street view panoramas
    """
    
    def __init__(
            self, 
            dataset_size=constants.DEFAULT_DATASET_SIZE, 
            api_key=constants.API_KEY, 
            image_size=constants.DEFAULT_IMAGE_SIZE, 
            fov=constants.DEFAULT_FOV,
            prompts=constants.DEFAULT_PROMPTS
        ) -> None:
        """
        Args:
            dataset_size (int, optional): size of dataset. Defaults to constants.DEFAULT_DATASET_SIZE.
            api_key (string, optional): google street view static api key. Defaults to constants.API_KEY.
            image_size (string, optional): image size in format <int>x<int>, max 640x640. Defaults to constants.DEFAULT_IMAGE_SIZE.
            fov (string, optional): image field of view. Defaults to constants.DEFAULT_FOV.
            prompts (list<string>, optional): prompts to generate random coordinates. Defaults to constants.DEFAULT_PROMPTS.
        """
        self.geolocator = Nominatim(user_agent='StreetViewDownloader')
        self.dataset_size = dataset_size
        self.api_key = api_key
        self.image_size = image_size
        self.fov = fov
        self.prompts = prompts
        self.coordinates = []
        self.pano_ids = []
        self.world_map = json.load(open(DirUtil.get_world_map_dir()))['features']

    def generate_coordinates(self) -> None:
        """Generates random coordinates using Google's Places API, coordinates are stored in self.coordinates
        """
        i = 0
        while len(self.coordinates) < self.dataset_size and i < len(self.prompts):
            url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={self.prompts[i]}&key={self.api_key}'
            results = requests.get(url)
            if (results.status_code == 200):
                results = results.json()
                results = results['results']
                j = 0
                while j < len(results) and len(self.coordinates) < self.dataset_size:
                    self.coordinates.append({results[j]['geometry']['location']['lat'], results[j]['geometry']['location']['lng']})
    
    def get_pano_ids_from_coordinates(self) -> None:
        """Gets panorama ids based on self.coordinates, ids are stored in self.pano_ids. Always call self.generate_coordinates prior to calling this method
        """
        for lat, lon in self.coordinates:
            panos = streetview.search_panoramas(lat, lon)
            if len(panos) > 0:
                self.pano_ids.append(panos[0])

    def download_random_street_view_images(self) -> None:
        """Downloads random street view images
        """
        # Create a directory to save the images
        images_dir = DirUtil.get_image_dir()
        os.makedirs(images_dir, exist_ok=True)

        # Retrieve and save the images
        for i in range(0, len(self.pano_ids)):
            pano_id = self.pano_ids[i].pano_id
            lat, lon = self.coordinates[i]
            url = f'https://maps.googleapis.com/maps/api/streetview?size={self.image_size}&pano={pano_id}&key={self.api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                image_name = f"{images_dir}/{lat}_{lon}.jpg"
                with open(image_name, 'wb') as pic:
                    pic.write(response.content)

        print("All images downloaded successfully.")