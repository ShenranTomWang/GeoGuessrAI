import os
import torch
import torch.nn as nn
import torchvision.models as models
import json

class Model(nn.Module):
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
    
    def forward(self, x:torch.Tensor) -> torch.Tensor:
        """Forward pass

        Args:
            x (torch.Tensor): input

        Returns:
            Tensor: output, 1d tensor
        """
        return self.model.forward(x)
    
    def save(self, path:str) -> None:
        """Saves model state to file

        Args:
            path (str): path to save file
        """
        os.makedirs(path, exist_ok=True)
        torch.save(self.model.state_dict(), f'{path}/ViT_B16.csv')
        with open(f'{path}/ViT_B16.json', 'w') as file:
            json.dump(self.to_json(), file, indent=4)
            
    def to_json(self) -> dict:
        """Converts self to json

        Returns:
            dict: parsed dictionary
        """
        return {
            'scale': self.scale
        }
        
    @staticmethod
    def coords_to_tensor(scale, lat, lon) -> 'torch.Tensor':
        """Converts coordinates to Tensor

        Args:
            scale (float): conversion scale
            lat (float): latitude
            lon (float): longitude

        Returns:
            torch.Tensor: converted probability map, 1d tensor
        """
        ret = torch.zeros((180 * scale, 360 * scale))
        lat, lon = int(lat * scale), int(lon * scale)
        ret[lat, lon] = 1
        ret = ret.view(-1)
        return ret
        
    @classmethod
    def load(cls, path:str) -> 'Model':
        """Loads model from path

        Args:
            path (str): path to load file
        """
        ckpd = torch.load(f'{path}/ViT_B16.csv')
        model = cls()
        model.model.load_state_dict(ckpd)
        return model