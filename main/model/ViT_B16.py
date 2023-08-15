import torch.nn as nn
import torchvision.models as models

class Model(nn.Module):
    """Transfer learning using ViT_B_16 model
    """
    
    def __init__(self, lat:int, lon:int) -> None:
        """
        Args:
            lat (int): number of divisions along latitude
            lon (int): number of divisions along longitude
        """
        super().__init__()
        self.lat = lat
        self.lon = lon
        self.model = models.vit_b_16(pretrained=True)
        self.model.heads[0] = nn.Linear(768, lat * lon)
    
    def forward(self, x):
        """Forward pass

        Args:
            x (Tensor): input

        Returns:
            Tensor: output
        """
        return self.model.forward(x)
    
        