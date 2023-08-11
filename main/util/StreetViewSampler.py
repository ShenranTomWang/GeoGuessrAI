import streetview
import os
import io
import json
import requests
from PIL import Image
from . import StreetViewSamplerConstants as constants
from . import DirUtil
from .Sample import Sample

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
        self.samples = []
        self.prompt_descriptor = 0
        self.download_descriptor = 0

    def sample(self, size_per_prompt:int=-1) -> None:
        """Generates random coordinates using Google's Places API and search for their corresponding panorama ids.
        Args:
            size_per_prompt (int, optional): number of samples collected per prompt, defaults to -1 meaning to collect all samples for each prompt
        """
        desired_len = self.sample_size + len(self.samples)
        while len(self.samples) < desired_len and self.prompt_descriptor < len(self.prompts):
            curr_prompt = self.prompts[self.prompt_descriptor]
            url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={curr_prompt}&key={self.api_key}'
            results = requests.get(url)
            if (results.status_code == 200):
                results = results.json()
                results = results['results']
                j = 0
                num_collected_samples_per_prompt = len(results) if size_per_prompt == -1 else size_per_prompt
                while j < num_collected_samples_per_prompt and j < len(results) and len(self.samples) < desired_len:
                    lat = results[j]['geometry']['location']['lat']
                    lon = results[j]['geometry']['location']['lng']
                    url = (
                        "https://maps.googleapis.com/maps/api/js/"
                        "GeoPhotoService.SingleImageSearch"
                        "?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{0:}!4d{1:}!2d50!3m10"
                        "!2m2!1sen!2sGB!9m1!1e2!11m4!1m3!1e2!2b1!3e2!4m10!1e1!1e2!1e3!1e4"
                        "!1e8!1e6!5m1!1e2!6m1!1e2"
                        "&callback=callbackfunc"
                    )
                    url = url.format(lat, lon)
                    resp = requests.get(url)
                    panos = streetview.search.extract_panoramas(resp.text)
                    if len(panos) > 0:
                        pano_id = panos[0].pano_id
                        coordinates = [lat, lon]
                        self.samples.append(Sample(pano_id, coordinates, curr_prompt))
                    else:
                        print(f'No panorama found at {lat}, {lon}')
                    j += 1
                if j < num_collected_samples_per_prompt:
                    print(f'Insufficient places found: wanted {num_collected_samples_per_prompt} but only found {j}')
            else:
                print(f'Prompt {self.prompts[self.prompt_descriptor]} responded with error code {results.status_code}')
            self.prompt_descriptor += 1
        if (len(self.samples) < self.sample_size):
            print(f'Sampled {len(self.samples)} samples due to insufficient resources. Please add more prompts or check validity of requests')
            self.sample_size = len(self.samples)
            
    def download_street_view_images(self, images_dir:str) -> None:
        """Downloads street view images. 
        Warning: 
            Images are generated depending on self.samples
        Args:
            images_dir (str): directory to save images to
        """
        os.makedirs(images_dir, exist_ok=True)
        while self.download_descriptor < len(self.samples):
            sample = self.samples[self.download_descriptor]
            content = None
            try:
                content = sample.get_street_view_image(self.image_size, self.api_key)
            except Exception:
                print(f'Cannot get street view image with pano id {sample.pano_id}')
                self.samples.pop(self.download_descriptor)
                continue
            lat, lon = sample.coordinates
            image_name = f"{images_dir}/{lat}_{lon}.jpg"
            with open(image_name, 'wb') as pic:
                pic.write(content)
            self.download_descriptor += 1

    def download_panoramas(self, images_dir:str) -> None:
        """Downloads panoramas. 
        Warning:
            Panoramas are generated depending on self.samples
            This method calls Google Street View Static API 4 times per panorama
        Args:
            images_dir (str): directory to save images to
        """
        os.makedirs(images_dir, exist_ok=True)
        while self.download_descriptor < len(self.samples):
            sample = self.samples[self.download_descriptor]
            image_data = sample.get_panorama(self.image_size, self.api_key)
            
            if len(image_data) != 4:
                print(f'Request failed while trying to get panorama id {sample.pano_id}')
                self.samples.pop(self.download_descriptor)
                continue
            
            images = []
            for data in image_data:
                image = Image.open(io.BytesIO(data))
                images.append(image)
            
            pano_w = self.image_width * 4
            pano_h = self.image_height
            pano = Image.new('RGB', (pano_w, pano_h))
            for i, image in enumerate(images):
                pano.paste(image, (i * self.image_width, 0))
            
            lat, lon = sample.coordinates
            image_name = f"{images_dir}/panorama_{lat}_{lon}.jpg"
            pano.save(image_name)
            self.download_descriptor += 1
        
    def save_sampler_status_metadata(self, metadata_dir:str, metadata_file_name:str=constants.DEFAULT_METADATA_FILE_NAME) -> None:
        """Saves sampler status metadata to a json file

        Args:
            metadata_dir (str): directory to save metadata file to
            metadata_file_name (str, optional): name of metadata file. Defaults to constants.DEFAULT_METADATA_FILE_NAME
        """
        os.makedirs(metadata_dir, exist_ok=True)
        with open(f'{metadata_dir}/{metadata_file_name}', 'w') as file:
            json.dump(self.to_json(), file, indent=4)
            
    @classmethod
    def from_json_file(cls, metadata_dir:str, sample_size:int, api_key:str, metadata_file_name:str=constants.DEFAULT_METADATA_FILE_NAME) -> 'StreetViewSampler':
        """Loads sampler status metadata from json file

        Args:
            cls: class
            metadata_dir (str): directory to metadata file
            sample_size (int): size of samples of current session
            api_key (str): your Google API key
            metadata_file_name (str, optional): name of metadata file. Defaults to constants.DEFAULT_METADATA_FILE_NAME.
        Returns:
            StreetViewSampler
        """
        jo = None
        with open(f'{metadata_dir}/{metadata_file_name}') as file:
            jo = json.load(file)
        product = cls(sample_size, api_key)
        product.fov = jo['fov']
        product.image_size = jo['image_size']
        product.prompt_descriptor = jo['prompt_descriptor']
        product.image_width = jo['image_width']
        product.image_height = jo['image_height']
        product.download_descriptor = jo['download_descriptor']
        product.samples = [Sample.from_json(sample) for sample in jo['samples']]
        return product
            
    def to_json(self) -> dict:
        """JSON encoder for StreetViewSampler
        
        Returns:
            dict: parsed dictionary
        """
        return {
            "download_descriptor": self.download_descriptor,
            "image_size": self.image_size,
            "fov": self.fov,
            "prompt_descriptor": self.prompt_descriptor,
            "image_width": self.image_width,
            "image_height": self.image_height,
            "samples": [sample.to_json() for sample in self.samples]
        }