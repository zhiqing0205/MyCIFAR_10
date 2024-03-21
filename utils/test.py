import os.path

import torch
from PIL import Image
from torch import nn
import torch.nn.functional as F
from torchvision import transforms

from MyCIFAR_10.settings import BASE_DIR


class MyCIFAR_10(nn.Module):
    def __init__(self):
        super(MyCIFAR_10, self).__init__()
        self.sequential = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Flatten(),
            nn.Linear(in_features=64 * 4 * 4, out_features=64),
            nn.Linear(in_features=64, out_features=10)
        )

    def forward(self, x):
        output = self.sequential(x)
        # softmax = Softmax(dim=0)
        # output = softmax(output)
        return output


def classify(path):
    model = MyCIFAR_10()
    model.load_state_dict(torch.load(os.path.join(os.path.join(BASE_DIR, 'utils'), 'models', 'model-21'), map_location=torch.device('cpu')))

    img = Image.open(path)
    compose = transforms.Compose([transforms.ToTensor(), transforms.Resize((32, 32))])

    img_tensor = compose(img)
    img_tensor = torch.reshape(img_tensor, (1, 3, 32, 32))

    model.eval()
    with torch.no_grad():
        output = model(img_tensor)

        classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        # print(output)
        t = F.softmax(torch.reshape(output, (10,)), dim=0)
        print(F.softmax(torch.reshape(output, (10,)), dim=0))
        print(output.argmax(1))
        print(classes[output.argmax(1)])
    return classes[output.argmax(1)], t[output.argmax(1)], t
