# ISPY2-Breast-MultimodalAI

**ISPY2-Breast-MultimodalAI** is a reproducible benchmark for **baseline prediction of pathologic complete response (pCR)** in breast cancer, integrating **dynamic contrast-enhanced MRI (DCE-MRI)** and **clinical variables** from the **I-SPY2 trial**.

The project focuses on the **clinically relevant pre-treatment scenario (baseline / T0)** and benchmarks **unimodal and multimodal learning approaches** under a consistent evaluation protocol.

---

## Motivation

Pathologic complete response (pCR) after neoadjuvant therapy is a strong prognostic marker in breast cancer. Accurate prediction of pCR at baseline could support treatment planning and patient stratification; however, predictive performance varies widely across imaging-only and multimodal approaches.

In practice, clinical variables often provide strong baseline performance, and it remains unclear how much additional value imaging-based deep learning models contribute when evaluated rigorously at the patient level.

This repository provides:

- a **clean and reproducible benchmark** on I-SPY2,
- **standardized train/validation/test splits**,
- strong **unimodal baselines**, and
- a **transparent multimodal fusion strategy**.

---

## Task Definition

### Primary task
Binary classification of **pathologic complete response (pCR)**:

> *Given baseline (pre-treatment) data, will the patient achieve pCR after neoadjuvant therapy?*

### Inputs (baseline only)

- **Imaging**: Baseline DCE-MRI  
  - Pre-contrast  
  - Early post-contrast  
  - Late post-contrast  
- **Clinical variables**: Baseline clinicopathologic features (e.g., age, menopause status, HR/HER2 status, subtype indicators)

### Output
- pCR (responder vs non-responder)

Longitudinal imaging and post-treatment information are **not used**.

---

## Dataset

### Imaging
Data are derived from the **BreastDCEDL** resource:

- Baseline DCE-MRI from the I-SPY2 cohort
- Three DCE phases provided per patient
- Official train / validation / test splits for pCR prediction

Source:  
https://github.com/naomifridman/BreastDCEDL

### Clinical Data
Baseline clinical and molecular annotations provided with I-SPY2, including:

- Age
- Menopause status
- Race indicators
- Hormone receptor (HR) and HER2 status
- Derived subtype indicators (e.g., triple-negative)

---

## MRI Representation (2.5D)

Each patient is represented using a **2.5D multi-phase strategy**:

- Central tumor slice determined using provided mask metadata
- Axial slices: \( z-1, z, z+1 \)
- Each slice contains 3 DCE phases

This results in a **9-channel input tensor** of shape:

(9, H, W)


---

## Models

### Unimodal MRI (CNN)
- 2D convolutional neural network
- Four convolutional blocks with ReLU and max pooling
- Global average pooling
- Fully connected head producing a single logit
- Binary cross-entropy with logits loss
- Early stopping based on validation AUROC

### Clinical-only baseline
- Logistic regression
- Baseline clinical variables only
- Class imbalance handled via class weighting

### Multimodal model
- MRI CNN used as a **fixed feature extractor**
- 256-dimensional MRI embedding extracted after global average pooling
- MRI embedding concatenated with clinical features
- Logistic regression trained on fused features

---

## Training and Evaluation

- Optimizer: Adam (CNN)
- Learning rate: \(1 \times 10^{-4}\)
- Batch size: 8
- Early stopping:
  - patience = 5
  - monitored on validation AUROC
- Learning rate scheduling: ReduceLROnPlateau

### Evaluation
- Metric: **AUROC**
- Evaluation performed at the **patient level**
- Final results reported on the held-out test set

---

## Results (Test AUROC)

| Model                          | AUROC |
|--------------------------------|-------|
| MRI-only (CNN)                 | 0.559 |
| Clinical-only (Logistic Reg.)  | 0.725 |
| Multimodal (MRI + Clinical)    | 0.726 |

---

## Repository Structure
```text
ISPY2-Breast-MultimodalAI/
│
├── notebooks/
│        │ 
│        ├── A1_mri_cnn.ipynb # MRI-only model
│        ├── A2_clinical_lr.ipynb # Clinical-only baseline
│        ├── B_multimodal.ipynb # Multimodal fusion
│
├── models/
│        ├── mri_cnn_model.py
│
├── preprocessing/
│        ├── transformations.py
│
├── README.md
```

---

## Reproducibility

All experiments were run using fixed data splits and deterministic preprocessing.  
Raw imaging and clinical data are **not redistributed** due to data usage agreements.

This repository provides scripts and notebooks required to reproduce all reported results from the original data sources.

---

## License and Disclaimer

This repository is provided for research and educational purposes only.  
The authors are not responsible for clinical use or interpretation of the results.
