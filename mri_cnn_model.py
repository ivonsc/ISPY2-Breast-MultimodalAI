import torch
import torch.nn as nn

class A1_MRI_CNN(nn.Module):
    def __init__(self, in_ch=3, dropout=0.5):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(in_ch, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        )

        self.gap = nn.AdaptiveAvgPool2d((1, 1))

        self.head = nn.Sequential(
            nn.Flatten(),          # (B,256,1,1) → (B,256)
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(128, 1)      # 1 logit (pCR)
        )
    
    def forward_features(self, x):
        x = self.features(x)
        x = self.gap(x)
        x = torch.flatten(x, 1)  # (B,256)
        return x
    
    def forward(self, x):
        f = self.forward_features(x)
        logit = self.head[1:](f)  
        return logit