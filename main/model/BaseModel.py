from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod, abstractproperty
import torch
import torch.nn as nn

class BaseModel(ABC, nn.Module):
    """Class abstracting a base model. Any model must inherit this abstract class
    """
    
    @abstractmethod
    def forward(self, x:torch.Tensor) -> torch.Tensor:
        """Forward pass

        Args:
            x (torch.Tensor): input

        Returns:
            Tensor: output, 1d tensor
        """
        pass
    
    @abstractmethod
    def save(self, path:str) -> None:
        """Saves model state to file

        Args:
            path (str): path to save file
        """
        pass
    
    @abstractmethod
    def to_json(self) -> dict:
        """Converts self to json

        Returns:
            dict: parsed dictionary
        """
        pass
    
    @abstractstaticmethod
    def coords_to_tensor(scale:float, lat:float, lon:float) -> 'torch.Tensor':
        """Converts coordinates to Tensor

        Args:
            scale (float): conversion scale
            lat (float): latitude
            lon (float): longitude

        Returns:
            torch.Tensor: converted probability map, 1d tensor
        """
        pass
    
    @abstractstaticmethod
    def prepareImage(img:'torch.Tensor', x:int, y:int) -> 'torch.Tensor':
        """Converts image to desired size

        Args:
            img (torch.Tensor): input image
            x (int): width
            y (int): height

        Returns:
            torch.Tensor: transformed image
        """
        pass
    
    @abstractclassmethod
    def load(cls, path:str) -> 'BaseModel':
        """Loads BaseModel from file at path

        Args:
            path (str): path to saved file

        Returns:
            BaseModel
        """
        pass