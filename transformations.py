import torchvision.transforms as T

class MinMaxNormalize:
    def __call__(self, x):
        # x: (C,H,W)
        eps = 1e-6
        x_min = x.amin(dim=(1,2), keepdim=True)
        x_max = x.amax(dim=(1,2), keepdim=True)
        return (x - x_min) / (x_max - x_min + eps)


train_tf = T.Compose([
    MinMaxNormalize(),
    T.RandomHorizontalFlip(p=0.5),
    T.RandomVerticalFlip(p=0.5),
    T.RandomRotation(10),
])

val_tf = T.Compose([
    MinMaxNormalize()
])