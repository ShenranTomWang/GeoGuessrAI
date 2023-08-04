import streetview
from geopy.geocoders import Nominatim
import os
import json
import requests
from . import StreetViewSamplerConstants as constants

class StreetViewSampler:
    """Class that abstracts a downloader of street view panoramas
    """
    
    def __init__(
            self, 
            dataset_size:int, 
            api_key:str, 
            image_size:str=constants.DEFAULT_IMAGE_SIZE, 
            fov:str=constants.DEFAULT_FOV,
            prompts:list=constants.DEFAULT_PROMPTS
        ) -> None:
        """
        Args:
            dataset_size (int): size of dataset.
            api_key (string): google street view static api key.
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

    def sample_coordinates(self) -> None:
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
            else:
                print(f'Prompt {self.prompts[i]} responded with error code {results.status_code}')
            i += 1
        if (len(self.coordinates) < self.dataset_size):
            print(f'Sampled {len(self.coordinates)} samples due to insufficient resources. Please add more prompts or check validity of requests')
            self.dataset_size = len(self.coordinates)
    
    def get_pano_ids_from_coordinates(self) -> None:
        """Gets panorama ids based on self.coordinates, ids are stored in self.pano_ids. Always call self.generate_coordinates prior to calling this method
        """
        for i in range(0, len(self.coordinates)):
            lat, lon = self.coordinates[i]
            panos = streetview.search_panoramas(lat, lon)
            if len(panos) > 0:
                self.pano_ids.append(panos[0])
            else:
                self.coordinates.pop(i)
                print(f'No panorama found at {lat}, {lon}')
        if (len(self.pano_ids) < self.dataset_size):
            print(f'Sampled {len(self.pano_ids)} samples. Some coordinates do not have a corresponding panorama')
            self.dataset_size = len(self.pano_ids)

    def download_street_view_images(self, images_dir:str) -> None:
        """Downloads street view images. Always call self.generate_coordinates and self.get_pano_ids_from_coordinates prior to calling this method
        Args:
            images_dir (string): directory to save images to
        """
        os.makedirs(images_dir, exist_ok=True)
        for i in range(0, self.dataset_size):
            pano_id = self.pano_ids[i].pano_id
            lat, lon = self.coordinates[i]
            url = f'https://maps.googleapis.com/maps/api/streetview?size={self.image_size}&pano={pano_id}&key={self.api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                image_name = f"{images_dir}/{lat}_{lon}.jpg"
                with open(image_name, 'wb') as pic:
                    pic.write(response.content)
        print("All images downloaded successfully.")
        
    def save_street_view_metadata(self, metadata_dir:str, metadata_file_name:str=constants.DEFAULT_METADATA_FILE_NAME):
        """Saves street view image metadata to a json file

        Args:
            metadata_dir (string): directory to save metadata file to
            metadata_file_name (string, optional): name of metadata file. Defaults to constants.DEFAULT_METADATA_FILE_NAME
        """
        os.makedirs(metadata_dir, exist_ok=True)
        jo = {
            "coordinates": self.coordinates,
            "pano_ids": self.pano_ids,
            "image_size": self.image_size,
            "fov": self.fov,
            "dataset_size": self.dataset_size
        }
        with open(f'{metadata_dir}/{metadata_file_name}', 'wb') as file:
            file.write(json.dumps(jo))