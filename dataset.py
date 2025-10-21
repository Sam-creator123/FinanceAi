from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import requests
from io import BytesIO
import PIL.Image as Image
from datasets import load_dataset

class FinFactDataset(Dataset):
    def __init__(self, hf_dataset, transform=None):
        self.dataset = hf_dataset
        self.transform = transform

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        text = item['claim']
        
        # Load image
        response = requests.get(item['image'])
        img = Image.open(BytesIO(response.content)).convert('RGB')
        if self.transform:
            img = self.transform(img)
        
        return {'text': text, 'image': img}

# Example transform
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

finfact_dataset = FinFactDataset(dataset['train'], transform=transform)
dataloader = DataLoader(finfact_dataset, batch_size=16, shuffle=True)
