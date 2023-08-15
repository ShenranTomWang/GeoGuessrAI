from torch.utils.data import Dataset
from . import DirUtil
from PIL import Image
import json
from torchvision import transforms
import torch

class Dataset(Dataset):
    def __init__(self, data:list) -> None:
        """
        Args:
            data (list): samples
        """
        self.data = data
        
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, index:int) -> tuple:
        sample = self.data[index]
        image_name = f'{DirUtil.get_image_dir()}/panorama_{sample.lat}_{sample.lon}_{sample.pano_id}.jpg'
        image = Image.open(image_name)
        transform = transforms.Compose([
            transforms.Resize((384, 384)),  # Resize the image to the desired input size
            transforms.ToTensor(),  # Convert the PIL image to a PyTorch tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the image
        ])
        input_image = transform(image)
        input_image = input_image.unsqueeze(0)
        input_image = input_image.permute(0, 2, 3, 1)
        input_tensor = torch.tensor(input_image)
        return input_tensor, sample.coordinates
    
    @classmethod
    def from_json(cls, path:str, metadata_file_name:str='metadata.json') -> 'Dataset':
        """Loads data from json file

        Args:
            path (str): path to file
            metadata_file_name (str, optional): name of metadata file. Defaults to 'metadata.json'.

        Returns:
            Dataset
        """
        jo = None
        with open(f'{path}/{metadata_file_name}') as file:
            jo = json.load(file)
        product = cls(jo['samples'])
        return product