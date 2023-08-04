import streetview
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
            api_key (str): google street view static api key.
            image_size (str, optional): image size in format <int>x<int>, max 640x640. Defaults to constants.DEFAULT_IMAGE_SIZE.
            fov (str, optional): image field of view. Defaults to constants.DEFAULT_FOV.
            prompts (list<str>, optional): prompts to generate random coordinates. Defaults to constants.DEFAULT_PROMPTS.
        """
        self.dataset_size = dataset_size
        self.api_key = api_key
        self.image_size = image_size
        self.fov = fov
        self.prompts = prompts
        self.coordinates = []
        self.pano_ids = []
        self.prompt_descriptor = 0

    def sample_coordinates(self) -> None:
        """Generates random coordinates using Google's Places API, coordinates are stored in self.coordinates
        """
        i = self.prompt_descriptor
        while len(self.coordinates) < self.dataset_size and i < len(self.prompts):
            url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={self.prompts[i]}&key={self.api_key}'
            results = requests.get(url)
            if (results.status_code == 200):
                results = results.json()
                results = results['results']
                j = 0
                while j < len(results) and len(self.coordinates) < self.dataset_size:
                    self.coordinates.append([results[j]['geometry']['location']['lat'], results[j]['geometry']['location']['lng']])
                    j += 1
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
                self.pano_ids.append(panos[0].pano_id)
            else:
                self.coordinates.pop(i)
                print(f'No panorama found at {lat}, {lon}')
        if (len(self.pano_ids) < self.dataset_size):
            print(f'Sampled {len(self.pano_ids)} samples. Some coordinates do not have a corresponding panorama')
            self.dataset_size = len(self.pano_ids)

    def download_street_view_images(self, images_dir:str) -> None:
        """Downloads street view images. Always call self.generate_coordinates and self.get_pano_ids_from_coordinates prior to calling this method
        Args:
            images_dir (str): directory to save images to
        """
        os.makedirs(images_dir, exist_ok=True)
        for i in range(0, self.dataset_size):
            pano_id = self.pano_ids[i]
            lat, lon = self.coordinates[i]
            url = f'https://maps.googleapis.com/maps/api/streetview?size={self.image_size}&pano={pano_id}&key={self.api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                image_name = f"{images_dir}/{lat}_{lon}.jpg"
                with open(image_name, 'wb') as pic:
                    pic.write(response.content)
        print("All images downloaded successfully.")
        
    def save_sampler_status_metadata(self, metadata_dir:str, metadata_file_name:str=constants.DEFAULT_METADATA_FILE_NAME) -> None:
        """Saves sampler status metadata to a json file

        Args:
            metadata_dir (str): directory to save metadata file to
            metadata_file_name (str, optional): name of metadata file. Defaults to constants.DEFAULT_METADATA_FILE_NAME
        """
        os.makedirs(metadata_dir, exist_ok=True)
        with open(f'{metadata_dir}/{metadata_file_name}', 'w') as file:
            file.write(json.dumps(self, default=StreetViewSampler.json_encoder))
            
    @staticmethod
    def load_sampler_status_metadata(metadata_dir:str, dataset_size:int, api_key:str, metadata_file_name:str=constants.DEFAULT_METADATA_FILE_NAME) -> 'StreetViewSampler':
        """Loads sampler status metadata from json file

        Args:
            metadata_dir (str): directory to metadata file
            dataset_size (int): size of dataset desired
            api_key (str): your Google API key
            metadata_file_name (str, optional): name of metadata file. Defaults to constants.DEFAULT_METADATA_FILE_NAME.
        """
        jo = None
        with open(f'{metadata_dir}/{metadata_file_name}') as file:
            jo = json.load(file)
        product = StreetViewSampler(dataset_size, api_key)
        product.coordinates = jo['coordinates']
        product.fov = jo['fov']
        product.image_size = jo['image_size']
        product.prompt_descriptor = jo['prompt_descriptor']
        return product
            
    @staticmethod
    def json_encoder(obj:'StreetViewSampler') -> object:
        return {
            "coordinates": obj.coordinates,
            "pano_ids": obj.pano_ids,
            "image_size": obj.image_size,
            "fov": obj.fov,
            "dataset_size": obj.dataset_size,
            "prompt_descriptor": obj.prompt_descriptor + 1
        }