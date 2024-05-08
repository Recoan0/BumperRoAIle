import torch
from torch import nn
import torch.nn.functional as F
import numpy as np


class FeedForwardNN(nn.Module):
    def __init__(self, in_dim, out_dim, hidden=64):
        super().__init__()
        self.layer1 = nn.Linear(in_dim, hidden)
        self.layer2 = nn.Linear(hidden, hidden//2)
        self.layer3 = nn.Linear(hidden//2, hidden//4)
        self.layer4 = nn.Linear(hidden//4, out_dim)

    def forward(self, obs):
        if isinstance(obs, np.ndarray):
            obs = torch.tensor(obs, dtype=torch.float32)

        a1 = F.relu(self.layer1(obs))
        a2 = F.relu(self.layer2(a1))
        output = self.layer3(a2)

        return output

