from torch.utils.data import Dataset
from .Sample import Sample
from PIL import Image
import json
from model.ViT_B16 import Model

class Dataset(Dataset):
    def __init__(self, data:list, width:int, height:int, model_scale:float, loading_dir:str) -> None:
        """
        Args:
            data (list): samples
            width (int): width per image
            height (int): height per image
            model_scale (float): scale of model
            loading_dir (str): directory name for loading data
        """
        self.data = data
        self.width = width
        self.height = height
        self.model_scale = model_scale
        self.index = 0
        self.loading_dir = loading_dir
        
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, index:int) -> tuple:
        sample = self.data[index]
        lat, lon = sample.coordinates[0], sample.coordinates[1]
        image_name = f'{self.loading_dir}/panorama_{lat}_{lon}_{sample.pano_id}.jpg'
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
        img = cropped[self.index]
        input_image = Model.prepareImage(img, 224, 224)
        label = Model.coords_to_tensor(self.model_scale, lat, lon)
        return input_image, label
    
    def incrementIndex(self) -> None:
        """Increment image get index
        """
        self.index += 1
        if self.index > 3:
            self.index = 0
    
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
        product = cls(samples, jo['image_width'], jo['image_height'], model_scale, path)
        return product