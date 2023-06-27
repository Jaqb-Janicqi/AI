import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


def get_tensor_state(encoded_board):
    return torch.tensor(encoded_board).unsqueeze(0).unsqueeze(0).float()


def get_policy(policy):
    return torch.softmax(policy, dim=1).squeeze(0).detach().numpy()


def get_value(value):
    return value.item()


class ResNet(nn.Module):
    def __init__(self, in_size, out_size, num_ResBlocks, num_hidden):
        super().__init__()
        self.start_block = nn.Sequential(
            nn.Conv2d(1, num_hidden, kernel_size=3, padding=1),
            nn.BatchNorm2d(num_hidden),
            nn.ReLU()
        )
        self.back_bone = nn.ModuleList(
            [ResBlock(num_hidden) for _ in range(num_ResBlocks)]
        )
        self.policy_head = nn.Sequential(
            nn.Conv2d(num_hidden, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32 * in_size, out_size)
        )
        self.value_head = nn.Sequential(
            nn.Conv2d(num_hidden, 3, kernel_size=3, padding=1),
            nn.BatchNorm2d(3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3 * in_size, 1),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.start_block(x)
        for block in self.back_bone:
            x = block(x)
        p = self.policy_head(x)
        v = self.value_head(x)
        return p, v


class ResBlock(nn.Module):
    def __init__(self, num_hidden):
        super().__init__()
        self.conv1 = nn.Conv2d(num_hidden, num_hidden,
                               kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(num_hidden)
        self.conv2 = nn.Conv2d(num_hidden, num_hidden,
                               kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(num_hidden)

    def forward(self, x):
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        x = F.relu(x)
        return x
