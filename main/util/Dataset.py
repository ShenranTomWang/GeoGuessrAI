from torch.utils.data import Dataset
from . import DirUtil
from .Sample import Sample
from PIL import Image
import json
from torchvision import transforms
import torch
import random
from model.ViT_B16 import Model

class Dataset(Dataset):
    def __init__(self, data:list, width:int, height:int, model_scale: float) -> None:
        """
        Args:
            data (list): samples
            width (int): width per image
            height (int): height per image
            model_scale (float): scale of model
        """
        self.data = data
        self.width = width
        self.height = height
        self.model_scale = model_scale
        
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, index:int) -> tuple:
        sample = self.data[index]
        lat, lon = sample.coordinates[0], sample.coordinates[1]
        image_name = f'{DirUtil.get_image_dir()}/panorama_{lat}_{lon}_{sample.pano_id}.jpg'
        image = Image.open(image_name)
        cropped = []
        w, _ = image.size
        for i in range(int(w / self.width)):
            left = i * self.width
            upper = 0
            right = (i + 1) * self.width
            lower = self.height
            cropped_image = image.crop((left, upper, right, lower))
            cropped.append(cropped_image)
            
        transform = transforms.Compose([
            transforms.Resize((224, 224)),  # Resize the image to the desired input size
            transforms.ToTensor(),  # Convert the PIL image to a PyTorch tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the image
        ])
        input_image = transform(cropped[random.randint(0, 3)])
        label = Model.coords_to_tensor(self.model_scale, lat, lon)
        return input_image, label
    
    @classmethod
    def from_json(cls, path:str, model_scale:float, metadata_file_name:str='metadata.json') -> 'Dataset':
        """Loads data from json file

        Args:
            path (str): path to file
            model_scale (float): model scale
            metadata_file_name (str, optional): name of metadata file. Defaults to 'metadata.json'.

        Returns:
            Dataset
        """
        jo = None
        with open(f'{path}/{metadata_file_name}') as file:
            jo = json.load(file)
        samples = [Sample.from_json(sample) for sample in jo['samples']]
        product = cls(samples, jo['image_width'], jo['image_height'], model_scale)
        return product