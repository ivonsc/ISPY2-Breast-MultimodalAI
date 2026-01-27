
# --------------------------------------------------------------------- #
#                       NIfTI I/O utilities                             #
# --------------------------------------------------------------------- #
import numpy as np
import nibabel as nib
import os
import re
import matplotlib.pyplot as plt

data_path="BreastDCEDL_ISPY2_min_crop"

deb = 1

def _ds_from_pid(pid: str) -> str:
    if "ISPY1" in pid:
        return "spy1"
    if ("ISPY2" in pid) or ("ACRIN-6698" in pid):
        return "spy2"
    if "Breast_MRI" in pid:
        return "duke"
    raise ValueError(f"Cannot infer dataset for pid={pid!r}")


def read_nifti(path: str) -> np.ndarray:
    return nib.load(path).get_fdata()

def _last_int(path):
    m = re.search(r"(\d+)\.nii\.gz$", path)
    return int(m.group(1)) if m else -1


def get_sorted_nifti_acquisitions(pid):

    nifti_path = os.path.join(data_path,'dce')

    ff = [x for x in os.listdir(nifti_path) if pid in x]
    if len(ff)==0: return None
    if deb:print(os.listdir(nifti_path)[:7],pid)
    if deb:print(ff)
    sorted_filenames = sorted(ff, key=_last_int)

    img = []
    for f in sorted_filenames:
        x = read_nifti(os.path.join(nifti_path, f))
        img.append(x)

    return img

def get_nifti_mask(pid: str):

    mask_path = os.path.join(data_path,'mask')

    mpath=mask_path

    ff = [x for x in os.listdir(mpath) if pid in x]

    if deb:print(ff)
    if len(ff)==0: return None

    f=ff[0]


    x = read_nifti(os.path.join(mpath, f))


    return x


def get_all_nifti_acquisitions(pid):
    nifti_path = os.path.join(data_path,'dce')

    dpath = nifti_path


    ff = [x for x in os.listdir(dpath) if pid in x]
    if len(ff)==0: return None
    if deb:print(os.listdir(dpath)[:7],pid)
    if deb:print(ff)


    img = []
    for f in ff:
        x = read_nifti(os.path.join(dpath, f))
        img.append(x)

    return img


def show_n_images(
    imgs,
    cmap="gray",
    titles=None,
    enlarge=4,
    mtitle=None,
    cut=False,
    axis_off=True,
    fontsize=15,
    cb=False,
):
    """Visualise *n* images side-by-side."""
    _ = plt.figure(figsize=(enlarge * len(imgs), enlarge * 2))
    for i, im in enumerate(imgs, 1):
        ax = plt.subplot(1, len(imgs), i)
        if cb and len(np.unique(im)) > 5:
            im = cont_br(im)
        ax.imshow(im[50:290, 75:450] if cut else im, cmap=cmap, origin="lower")
        if titles is not None:
            ax.set_title(titles[i - 1], fontsize=fontsize)
        if axis_off:
            ax.axis("off")
    if mtitle:
        plt.suptitle(mtitle, fontsize=fontsize + 2)
    plt.tight_layout(); plt.show()
