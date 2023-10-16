import os
import torch
import torch.nn as nn
import torchvision.models as models
import json
from torchvision import transforms
import torch
from .BaseModel import BaseModel as BaseModel

class Model(BaseModel):
    """Transfer learning using ViT_B_16 model
    """
    
    def __init__(self, scale:float) -> None:
        """
        Args:
            scale (float): scaling factor of map
        """
        super().__init__()
        self.model = models.vit_b_16(pretrained=True)
        self.scale = scale
        self.model.heads[0] = nn.Linear(768, 180 * scale * 360 * scale)
        self.model.heads.append(nn.Softmax())
    
    def forward(self, x:torch.Tensor) -> torch.Tensor:
        return self.model.forward(x)
    
    def save(self, path:str) -> None:
        os.makedirs(path, exist_ok=True)
        torch.save(self.model.state_dict(), f'{path}/ViT_B16.csv')
        with open(f'{path}/ViT_B16.json', 'w') as file:
            json.dump(self.to_json(), file, indent=4)
            
    def to_json(self) -> dict:
        return {
            'scale': self.scale
        }
        
    @staticmethod
    def coords_to_tensor(scale:float, lat:float, lon:float) -> 'torch.Tensor':
        ret = torch.zeros((180 * scale, 360 * scale))
        lat, lon = int(lat * scale), int(lon * scale)
        ret[lat, lon] = 1
        ret = ret.view(-1)
        return ret

    @staticmethod
    def prepareImage(img, x, y):
        transform = transforms.Compose([
            transforms.Resize((x, y)),  # Resize the image to the desired input size
            transforms.ToTensor(),  # Convert the PIL image to a PyTorch tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the image
        ])
        input_image = transform(img)
        return input_image
        
    @classmethod
    def load(cls, path:str) -> 'Model':
        jo = None
        with open(f'{path}/ViT_B16.json') as file:
            jo = json.load(file)
        ckpd = torch.load(f'{path}/ViT_B16.csv')
        model = cls(jo['scale'])
        model.model.load_state_dict(ckpd)
        return model