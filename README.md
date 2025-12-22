# ISPY2-Breast-MultimodalAI

**ISPY2-Breast-MultimodalAI** is a reproducible benchmark for **multimodal prediction of neoadjuvant treatment response (pathologic complete response, pCR)** in breast cancer, integrating **baseline DCE-MRI, transcriptomic data, and clinical variables** from the I-SPY2 trial.

The project focuses on the **clinically relevant pre-treatment scenario (T0)**, where treatment decisions are made, and systematically compares **unimodal and multimodal models**, as well as **self-supervised vs fully supervised learning** for medical imaging.

---

## Motivation

Predicting response to neoadjuvant chemotherapy (NAC) is a central problem in precision oncology. While previous studies have explored imaging-based or molecular predictors independently, **there is currently no standardized, public benchmark that evaluates multimodal models combining imaging, transcriptomics, and clinical data at baseline** in I-SPY2.

This repository addresses that gap by providing:

* a **clean benchmark definition**,
* **standardized data splits**,
* **multiple baseline models**, and
* a **fair comparison of learning strategies**.

---

## Task Definition

**Primary task**
Binary classification of **pathologic complete response (pCR)**:

> *Given baseline (pre-treatment) data, will the patient achieve pCR after neoadjuvant therapy?*

**Inputs (T0 only):**

* **Imaging**: Baseline DCE-MRI (pre-contrast, early post-contrast, late post-contrast)
* **Transcriptomics**: Baseline gene expression profiles (I-SPY2-990)
* **Clinical variables**: Baseline clinical and molecular features (e.g., HR/HER2 status, age)

**Output:**

* pCR (responder vs non-responder)

Longitudinal imaging (T1/T2/T3) is **not included in the core benchmark**, as molecular data are only available at baseline. Longitudinal analyses are considered optional extensions.

---

## Datasets

### Imaging

* **BreastDCEDL**

  * Curated baseline DCE-MRI (T0) from I-SPY1, I-SPY2, and Duke cohorts
  * Pre-contrast, early, and late post-contrast phases provided as separate channels
  * Official train/validation/test splits for pCR prediction

### Transcriptomics and Clinical Data

* **I-SPY2-990 (GSE194040)**

  * Baseline transcriptomic profiles
  * Clinical variables and pCR labels
  * Treatment arm information (used for analysis, not modeled as a primary input)

### Multimodal Cohort

The **multimodal benchmark cohort** is defined as the intersection of:

```
Baseline DCE-MRI + transcriptomics + clinical data + pCR
```

Unimodal experiments use the largest available cohorts per modality.

---

## Benchmark Structure

### Unimodal Models

* Imaging-only (supervised)
* Imaging-only (self-supervised pretraining + fine-tuning)
* Transcriptomics-only (MLP)
* Clinical-only (MLP)

### Multimodal Models

* Imaging (supervised) + transcriptomics + clinical
* Imaging (SSL-pretrained) + transcriptomics + clinical

### Fusion Strategy

* **Intermediate fusion**

  * Separate encoders per modality
  * Latent representations fused via concatenation or attention-based modules

---

## Self-Supervised Learning (SSL)

Self-supervised learning is applied **exclusively to the imaging encoder**, leveraging large-scale unlabeled DCE-MRI data.

* SSL is **not applied** to transcriptomic or clinical modalities
* SSL-pretrained encoders are compared against fully supervised counterparts in:

  * imaging-only models
  * multimodal models

This design allows a clean and interpretable evaluation of SSL benefits.

---

## Evaluation

* Primary metric: **AUROC**
* Secondary metrics: accuracy, sensitivity, specificity, calibration
* Evaluation performed using:

  * Official BreastDCEDL splits (when applicable)
  * Stratified cross-validation for multimodal cohorts

---

## Repository Goals

This repository aims to:

* Provide a **transparent and reproducible benchmark**
* Enable **fair comparison** between unimodal and multimodal approaches
* Serve as a **reference implementation** for multimodal learning in neoadjuvant breast cancer
* Facilitate future extensions (e.g., longitudinal imaging, treatment-aware models)

---

## Repository Structure (high-level)

```
ISPY2-Breast-MultimodalAI/
│
├── data/                # Download scripts and metadata (no raw data)
├── preprocessing/       # MRI, RNA, and clinical preprocessing
├── models/              # Unimodal and multimodal models
├── benchmarks/          # Training and evaluation scripts
├── notebooks/           # Exploratory analysis and sanity checks
├── experiments/         # Configuration files for experiments
├── README.md
```

---

## Disclaimer

Due to data usage agreements, **raw datasets are not redistributed**.
This repository provides scripts and instructions to download and preprocess the data from the original sources.



* ayudarte a escribir el **abstract del paper**,
* o definir los **nombres oficiales de los experimentos** (Model A, Model B, etc.) para que todo quede perfectamente alineado.
