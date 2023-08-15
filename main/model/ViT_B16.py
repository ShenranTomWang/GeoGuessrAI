import torch
import torch.nn as nn
import torchvision.models as models

class Model(nn.Module):
    """Transfer learning using ViT_B_16 model
    """
    
    def __init__(self, num_classes:int) -> None:
        """
        Args:
            num_classes (int): number of outputs
        """
        super().__init__()
        self.model = models.vit_b_16(pretrained=True)
        self.model.heads[0] = nn.Linear(768, num_classes)
    
    def forward(self, x:torch.Tensor) -> torch.Tensor:
        """Forward pass

        Args:
            x (torch.Tensor): input

        Returns:
            Tensor: output
        """
        return self.model.forward(x)
    
    def save(self, path:str) -> None:
        """Saves model state to file

        Args:
            path (str): path to save file
        """
        torch.save(self.model.state_dict(), f'{path}/ViT_B16.csv')
        
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