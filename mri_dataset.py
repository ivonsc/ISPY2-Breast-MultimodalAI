from torch.utils.data import Dataset
import numpy as np
import torch
from ionifti import get_sorted_nifti_acquisitions

class MRIPatient25DDataset(Dataset):
    def __init__(self, df, transform=None, k=3, cache=True):
        """
        k=3 -> usa z-1, z, z+1
        Devuelve 1 item por paciente: (9,H,W)
        """
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.k = k
        assert k % 2 == 1, "k must be odd"
        self.cache = {} if cache else None

    def __len__(self):
        return len(self.df)
    
    def _load_pid(self, pid):
        d = get_sorted_nifti_acquisitions(pid)
        if d is None or len(d) < 3:
            raise RuntimeError(f"Missing DCE for {pid}")
        # guarda solo las 3 fases como float32 para ahorrar RAM
        return [np.asarray(d[i], dtype=np.float32) for i in range(3)]  # [pre,early,late]
    
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        pid = row["pid"]
        y = torch.tensor([float(row["pCR"])], dtype=torch.float32)

        pmask = int((row["mask_start"] + row["mask_end"]) // 2)
        
        if self.cache is not None:
            if pid not in self.cache:
                self.cache[pid] = self._load_pid(pid)
            d = self.cache[pid]
        else:
            d = self._load_pid(pid)

        nz = d[0].shape[0]
        half = self.k // 2
        zs = [max(0, min(pmask + off, nz - 1)) for off in range(-half, half + 1)]  # [z-1,z,z+1]

        # construye 9 canales: (3 fases) x (k slices)
        chans = []
        for z in zs:
            chans.append(d[0][z])  # pre
            chans.append(d[1][z])  # early
            chans.append(d[2][z])  # late

        x = np.stack(chans, axis=0).astype(np.float32)  # (9,H,W)
        x = torch.from_numpy(x)

        if self.transform:
            x = self.transform(x)

        return x, y, pid
