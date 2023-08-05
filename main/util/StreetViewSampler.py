import streetview
import os
import io
import json
import requests
from PIL import Image
from . import StreetViewSamplerConstants as constants

class StreetViewSampler:
    """Class that abstracts a downloader of street view panoramas
    """
    
    def __init__(
            self, 
            sample_size:int, 
            api_key:str, 
            image_width:int=constants.DEFAULT_IMAGE_WIDTH,
            image_height:int=constants.DEFAULT_IMAGE_HEIGHT,
            fov:str=constants.DEFAULT_FOV,
            prompts:list=constants.DEFAULT_PROMPTS
        ) -> None:
        """
        Args:
            sample_size (int): sample size of current sample session
            api_key (str): your Google API key
            image_width (int, optional): width of street view image. Defaults to constants.DEFAULT_IMAGE_WIDTH.
            image_height (int, optional): height of street view image. Defaults to constants.DEFAULT_IMAGE_HEIGHT.
            fov (str, optional): field of view. Defaults to constants.DEFAULT_FOV.
            prompts (list, optional): prompts to generate places. Defaults to constants.DEFAULT_PROMPTS.
        """
        self.sample_size = sample_size
        self.api_key = api_key
        self.image_width = image_width
        self.image_height = image_height
        self.image_size = f'{image_width}x{image_height}'
        self.fov = fov
        self.prompts = prompts
        self.coordinates = []
        self.pano_ids = []
        self.prompt_descriptor = 0
        self.download_descriptor = 0

    def sample(self) -> None:
        """Generates random coordinates using Google's Places API and search for their corresponding panorama ids. Coordinates are stored in self.coordinates, pano ids are stored in self.pano_ids
        """
        self.download_descriptor = len(self.pano_ids)
        while len(self.coordinates) < self.sample_size and self.prompt_descriptor < len(self.prompts):
            url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={self.prompts[self.prompt_descriptor]}&key={self.api_key}'
            results = requests.get(url)
            if (results.status_code == 200):
                results = results.json()
                results = results['results']
                j = 0
                while j < len(results) and len(self.coordinates) < self.sample_size:
                    lat = results[j]['geometry']['location']['lat']
                    lon = results[j]['geometry']['location']['lng']
                    panos = streetview.search_panoramas(lat, lon)
                    if len(panos) > 0:
                        self.pano_ids.append(panos[0].pano_id)
                        self.coordinates.append([lat, lon])
                    else:
                        print(f'No panorama found at {lat}, {lon}')
                    j += 1
            else:
                print(f'Prompt {self.prompts[self.prompt_descriptor]} responded with error code {results.status_code}')
            self.prompt_descriptor += 1
        if (len(self.coordinates) < self.sample_size):
            print(f'Sampled {len(self.coordinates)} samples due to insufficient resources. Please add more prompts or check validity of requests')
            self.sample_size = len(self.coordinates)
            
    def download_street_view_images(self, images_dir:str) -> None:
        """Downloads street view images. 
        Warning: 
            Images are generated depending on self.coordinates and self.pano_ids
        Args:
            images_dir (str): directory to save images to
        """
        os.makedirs(images_dir, exist_ok=True)
        for i in range(self.download_descriptor, len(self.pano_ids)):
            pano_id = self.pano_ids[i]
            lat, lon = self.coordinates[i]
            url = f'https://maps.googleapis.com/maps/api/streetview?size={self.image_size}&pano={pano_id}&key={self.api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                image_name = f"{images_dir}/{lat}_{lon}.jpg"
                with open(image_name, 'wb') as pic:
                    pic.write(response.content)

    def download_panoramas(self, images_dir:str) -> None:
        """Downloads panoramas. 
        Warning:
            Panoramas are generated depending on self.coordinates and self.pano_ids
            This method calls Google Street View Static API 4 times per panorama
        Args:
            images_dir (str): directory to save images to
        """
        os.makedirs(images_dir, exist_ok=True)
        coord_counter = 0
        for i in range(self.download_descriptor, len(self.pano_ids)):
            pano_id = self.pano_ids[i]
            lat, lon = self.coordinates[coord_counter]
            image_data = []
            
            for heading in constants.DEFAULT_HEADINGS:
                url = f'https://maps.googleapis.com/maps/api/streetview?size={self.image_size}&heading={heading}&pano={pano_id}&key={self.api_key}'
                response = requests.get(url)
                if response.status_code == 200:
                    image_data.append(response.content)
                else:
                    print(f'Error {response.status_code} occurred at location {lat}, {lon} at heading {heading}')
                    
            images = []
            for data in image_data:
                image = Image.open(io.BytesIO(data))
                images.append(image)
            
            pano_w = self.image_width * 4
            pano_h = self.image_height
            pano = Image.new('RGB', (pano_w, pano_h))
            for i, image in enumerate(images):
                pano.paste(image, (i * self.image_width, 0))
            
            image_name = f"{images_dir}/panorama_{lat}_{lon}.jpg"
            pano.save(image_name)
            coord_counter += 1
        
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
    def load_sampler_status_metadata(metadata_dir:str, sample_size:int, api_key:str, metadata_file_name:str=constants.DEFAULT_METADATA_FILE_NAME) -> 'StreetViewSampler':
        """Loads sampler status metadata from json file

        Args:
            metadata_dir (str): directory to metadata file
            sample_size (int): size of samples of current session
            api_key (str): your Google API key
            metadata_file_name (str, optional): name of metadata file. Defaults to constants.DEFAULT_METADATA_FILE_NAME.
        """
        jo = None
        with open(f'{metadata_dir}/{metadata_file_name}') as file:
            jo = json.load(file)
        product = StreetViewSampler(sample_size, api_key)
        product.fov = jo['fov']
        product.image_size = jo['image_size']
        product.prompt_descriptor = jo['prompt_descriptor']
        product.pano_ids = jo['pano_ids']
        product.image_width = jo['image_width']
        product.image_height = jo['image_height']
        product.download_descriptor = jo['download_descriptor']
        return product
            
    @staticmethod
    def json_encoder(obj:'StreetViewSampler') -> object:
        return {
            "download_descriptor": obj.download_descriptor,
            "pano_ids": obj.pano_ids,
            "image_size": obj.image_size,
            "fov": obj.fov,
            "sample_size": obj.sample_size,
            "prompt_descriptor": obj.prompt_descriptor,
            "image_width": obj.image_width,
            "image_height": obj.image_height
        }