from model.ViT_B16 import Model
from util.Dataset import Dataset
import util.DirUtil as DirUtil
from torch.utils.data import DataLoader
import torch
import torch.nn as nn

device = 'cuda' if torch.cuda.is_available() else 'cpu'
num_epochs = 2
batch_size = 10

scale = 1
dataset = Dataset.from_json(DirUtil.get_image_dir(), scale)
tr_set = DataLoader(dataset, batch_size, shuffle=True)
model = Model(scale).to(device)

for name, param in model.model.named_parameters():
    if not name == 'heads.head.weight':
        param.requires_grad == False

criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
for epoch in range(num_epochs):
    model.train()
    batch_count = 0
    for inputs, labels in tr_set:
        optimizer.zero_grad()
        inputs, labels = inputs.to(device), labels.to(device)
        preds = model(inputs)
        loss = criterion(preds, labels)
        loss.backward()
        optimizer.step()
        print(f'Batch: {batch_count + 1}/{batch_size}, Loss: {loss.item()}')
        batch_count += 1
        if (batch_count) % 10 == 0:
            batch_count = 0
    print(f'Epoch: {epoch + 1}/{num_epochs}, Loss: {loss.item()}')
model.save(DirUtil.get_model_dir())