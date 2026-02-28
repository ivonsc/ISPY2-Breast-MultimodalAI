from mri_dataset import MRIPatient25DDataset
from torch.utils.data import DataLoader
import pandas as pd
from transformations import train_tf, val_tf
# Load metadata and preprocess
df=pd.read_csv('metadata/BreastDCEDL_metadata_min_crop.csv')
df.info()

df = df[df["pid"].str.contains("ISPY2|ACRIN", regex=True)]
print("After cohort filter:", df.shape)

required_cols = ["pid", "pCR", "mask_start", "mask_end", "test"]
df = df.dropna(subset=required_cols)
print("After NaN filter:", df.shape)
df = df.reset_index(drop=True)

# Import and load Train, Validation and Test set

df_train = df[df["test"] == 0]
df_val   = df[df["test"] == 2]
df_test  = df[df["test"] == 1]

train_set = MRIPatient25DDataset(df_train, transform=train_tf, cache=True)
val_set   = MRIPatient25DDataset(df_val, transform=val_tf, cache=True)
test_set  = MRIPatient25DDataset(df_test, transform=val_tf, cache=True)

train_loader = DataLoader(
    train_set,
    batch_size=8,
    shuffle=True,
    num_workers=0,
    pin_memory=True
)

val_loader = DataLoader(
    val_set,
    batch_size=8,
    shuffle=False,
    num_workers=0,
    pin_memory=True
)

test_loader = DataLoader(
    test_set,
    batch_size=8,
    shuffle=False,
    num_workers=0,
    pin_memory=True
)