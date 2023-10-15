from model.ViT_B16 import Model
from util.Dataset import Dataset
import util.DirUtil as DirUtil
from torch.utils.data import DataLoader
import torch
import torch.nn as nn

device = 'cuda' if torch.cuda.is_available() else 'cpu'
num_epochs = 2
num_directions = 4
batch_size = 10

scale = 1
dataset = Dataset.from_json(DirUtil.get_testing_image_dir(), scale)
tt_set = DataLoader(dataset, batch_size, shuffle=True)
model = Model.load(DirUtil.get_model_dir()).to(device)

criterion = nn.MSELoss()
model.eval()
total_loss = 0
for index, (inputs, labels) in enumerate(tt_set):
    inputs, labels = inputs.to(device), labels.to(device)
    with torch.no_grad():
        preds = model(inputs)
        loss = criterion(preds, labels)
    total_loss += loss.item()
    print(f'Batch index: {index + 1}, Loss: {loss.item()}')