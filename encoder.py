import torch.nn as nn
import torch.nn.functional as F

class SmallCNNEncoder(nn.Module):
    """
    Encoder 2D simple para inputs multi-canal (por ejemplo C=9).
    Reemplázalo por tu A1_MRI_CNN backbone si quieres.
    """
    def __init__(self, in_ch=9, feat_dim=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.fc = nn.Linear(128, feat_dim)

    def forward(self, x):
        x = self.net(x).flatten(1)
        x = self.fc(x)
        return x
    
class MRIClassifier(nn.Module):
    def __init__(self, encoder, feat_dim=256):
        super().__init__()
        self.encoder = encoder
        self.classifier = nn.Linear(feat_dim, 1)  # binario

    def forward(self, x):
        h = self.encoder(x)
        logits = self.classifier(h)
        return logits.squeeze(1)