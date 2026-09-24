# 💳 AI Credit Risk & Loan Default Intelligence Platform

Predicting whether a loan applicant will **default** — and serving that prediction through a bilingual, client-facing web app.

## 🧭 Overview

This project builds an end-to-end machine learning platform on the **Home Credit Default Risk** dataset to estimate an applicant's probability of loan default, and ships it as **Smart Credit Advisor**: a Streamlit wizard for people with zero data-science background, available in Arabic (RTL), English, German, and French.

The goal isn't just to build a model — it is to develop a **leak-free, cost-aware, production-oriented pipeline**: every statistic and encoder is fit on the training split only, the operating decision threshold is chosen from a business cost matrix rather than a default 0.5 cut-off, and two independent model families (classical ML and deep learning) are benchmarked head-to-head under identical conditions before either one is trusted.

## 🗂️ Repository Structure

```text
AI-Credit-Risk-Loan-Default-Platform/
│
├── app/
│   ├── app.py                      # Streamlit client-facing app ("Smart Credit Advisor")
│   ├── i18n.py                     # Translation strings & language config (ar/en/de/fr)
│   └── prediction_engine.py        # UI-agnostic inference engine (loads & runs saved artifacts)
│
├── data/
│   ├── raw/
│   │   └── home-credit-default-risk/
│   │       └── [Raw Home Credit dataset — not included]
│   │
│   └── processed/
│       ├── final_feature_dataset.csv
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
│
├── models/
│   └── versioned_artifacts/
│       ├── best_classical_model.joblib
│       ├── best_mlp_model.keras
│       ├── logistic_regression_final.joblib
│       ├── mlp_calibrator.joblib
│       ├── mlp_preprocessing_pipeline.joblib
│       ├── preprocessing_pipeline.joblib
│       └── xgboost_final.joblib
│           └── [Excluded from GitHub — >100 MB]
│
├── notebooks/
│   ├── Data_Collection.ipynb       # 01 — raw table aggregation
│   ├── feature_preparation.ipynb   # 02 — EDA & feature preparation
│   ├── ML_Models.ipynb             # 03 — classical ML experiments
│   └── DL.ipynb                    # 04 — deep learning (MLP) experiments
│
├── reports/
│   ├── figures/
│   └── [Evaluation reports, metrics & metadata]
│
├── requirements.txt
└── .gitignore
```

> **Note:** The raw dataset and the largest trained-model files are excluded from the repository because of their size. The notebooks contain the complete, reproducible data-processing and modeling workflow.

## 🔄 Pipeline

### 1. Data Collection

**Notebook:** `notebooks/Data_Collection.ipynb`

* Loads the seven raw Home Credit tables and discovers their primary-key/foreign-key relationships programmatically.
* Aggregates `bureau_balance` → `bureau` → applicant level, and `POS_CASH_balance` / `credit_card_balance` / `installments_payments` → `previous_application` → applicant level.
* Merges everything onto `application_train` at one row per `SK_ID_CURR`.
* Asserts row-count preservation after **every** merge, to catch silent duplication bugs immediately rather than downstream.

### 2. EDA & Feature Preparation

**Notebook:** `notebooks/feature_preparation.ipynb`

The dataset was audited for:

* Missing values (including "no prior loans" NaN patterns in bureau/previous-application aggregates)
* Constant and near-constant features
* Target leakage (rule-based, domain audit — before any `TARGET` statistic is computed)
* Duplicate/identifier columns

An 80/20 **stratified** Train/Test split was locked in before any target-relative statistic was computed, and all further EDA and preprocessing (imputers, encoders, scaler) were fit on the training split only.

### 3. Target Leakage & Identifier Audit

A recurring question drove feature selection throughout:

> *Would this information realistically be available at the moment the model needs to score the applicant?*

Identifier columns (`SK_ID_CURR`, `SK_ID_BUREAU`, `SK_ID_PREV`, …) were excluded from modeling, and every engineered feature was checked against the project's four leakage categories before being kept.

### 4. Classical ML Modeling

**Notebook:** `notebooks/ML_Models.ipynb`

* Benchmarked via 5-fold **stratified** cross-validation using out-of-fold predictions.
* Models: Logistic Regression, Decision Tree, Random Forest, XGBoost — each tried with `class_weight` and with SMOTE.
* **PR-AUC** as the primary selection metric (default rate is ~8%, so ROC-AUC/accuracy are less informative for the minority class).
* Top two candidates tuned with `RandomizedSearchCV` (PR-AUC scoring, Test never touched).
* Decision threshold chosen by minimizing a **business cost matrix** (`FN_COST = 10`, `FP_COST = 1`) on out-of-fold predictions.
* Both tuned candidates calibrated (Platt/isotonic, picked by lowest Brier score).
* Final champion scored **once** on the locked Test set.

### 5. Deep Learning Modeling

**Notebook:** `notebooks/DL.ipynb`

* Same features, same Train/Test split, same cost matrix as the classical track — for a fair head-to-head comparison.
* A 70/15/15 (sub-train / validation / calibration) split carved out of Train.
* A regularized MLP (Dense + ReLU + Dropout + L2 + sigmoid output), trained with `class_weight` (no SMOTE), `EarlyStopping` + `ReduceLROnPlateau` monitoring **validation PR-AUC**, best weights restored.
* One additional architecture variant tried (wider first layer, stronger dropout) — not a full hyperparameter sweep.
* Best model selected by validation PR-AUC, calibrated on the held-out calibration split, threshold re-optimized on the same cost matrix, then scored **once** on the locked Test set.

### 6. Serving

**App:** `app/`

* `prediction_engine.py` only *loads* what the notebooks already saved (models, preprocessors, calibrators, thresholds) and runs inference — it never trains, tunes, or recalibrates anything.
* A practical, applicant-facing subset of fields is mapped onto the model's full ~586-feature schema; anything the form doesn't collect is left `NaN` and handled by the saved pipeline's own imputers, exactly as it would handle a real applicant's missing data.
* `app.py` renders the result as a plain-language risk tier — no model names, thresholds, or statistical jargon reach the end user.

## 📊 Results

### Classical ML — Baseline Comparison (5-fold CV, out-of-fold, best strategy per model)

| Model | Imbalance Strategy | ROC-AUC | PR-AUC | Recall@0.5 | Precision@0.5 | F1@0.5 |
|---|---|---:|---:|---:|---:|---:|
| Logistic Regression | class_weight | 0.7693 | 0.2463 | 0.6977 | 0.1740 | 0.2785 |
| XGBoost | smote | 0.7499 | 0.2307 | 0.0721 | 0.4030 | 0.1223 |
| Random Forest | class_weight | 0.7403 | 0.2071 | 0.0017 | 0.5397 | 0.0034 |
| Decision Tree | class_weight | 0.7047 | 0.1832 | 0.6637 | 0.1428 | 0.2350 |

Logistic Regression (class_weight) and XGBoost (SMOTE) were carried forward for tuning, threshold optimization, and calibration.

### Final Models — Locked Test Set (calibrated, cost-optimal threshold = 0.09)

| Model | PR-AUC | ROC-AUC | Recall | Precision | F1 | Brier | Business Cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Logistic Regression** (classical champion) | 0.2569 | 0.7747 | 0.6731 | 0.1816 | 0.2860 | 0.0668 | 31,293 |
| **MLP** (wide, 716→512→128→1) | 0.2475 | 0.7691 | 0.6645 | 0.1858 | 0.2904 | 0.0671 | 31,118 |

The two tracks land within noise of each other: Logistic Regression was kept as the classical champion (best PR-AUC), while the MLP edges it slightly on business cost and F1 — the app can serve either, since both are saved with their own calibrator and threshold.

The threshold was deliberately tuned far below the default 0.50 (down to **0.09**), because in this business setting a missed default (`FN_COST = 10`) is far costlier than a false alarm (`FP_COST = 1`) — trading precision for the recall needed to actually catch high-risk applicants.

## 🖥️ Application — Smart Credit Advisor

A Streamlit wizard (`app/app.py`) lets a non-technical user get an estimated risk read on a loan:

* Collects a practical subset of inputs (income, loan amount, employment length, family situation, etc.) rather than the full feature schema.
* Never shows model names, probabilities-as-decimals, or thresholds — only a plain-language risk tier: **Low / Moderate / High / Very High Risk**.
* Fully translated and RTL-aware: Arabic 🇪🇬, English 🇬🇧, German 🇩🇪, French 🇫🇷.
* Falls back to the classical champion automatically if the MLP artifacts aren't present.

## 🛠️ Tech Stack

* **Python**
* **pandas / NumPy**
* **scikit-learn**
* **XGBoost**
* **imbalanced-learn (SMOTE)**
* **TensorFlow / Keras**
* **Streamlit**
* **Matplotlib / Seaborn**
* **Joblib**
* **Jupyter Notebook**

## 🚀 Key Takeaways

* Built an end-to-end ML platform, from raw relational tables to a deployed, multilingual client-facing app.
* Aggregated seven raw Home Credit tables into a single leak-audited, applicant-level dataset with row-count assertions after every merge.
* Designed the feature set and every preprocessing step around a strict "fit on Train only" discipline.
* Benchmarked four classical models and an MLP under identical splits, features, and cost assumptions for a fair comparison.
* Replaced the default 0.5 cut-off with a cost-matrix-optimized decision threshold, tuned only on Train/validation data.
* Calibrated both final models so their outputs are usable as real probabilities, not just ranking scores.
* Cleanly separated inference (`prediction_engine.py`) from training — the serving layer can never accidentally retrain or leak Test data.

## 📌 Dataset

This project uses the **Home Credit Default Risk** dataset.

Dataset source: [Home Credit Default Risk — Kaggle](https://www.kaggle.com/c/home-credit-default-risk)

The raw dataset is not included in this repository — download it and place it under `data/raw/home-credit-default-risk/`.

## 🔮 Future Work

* Add SHAP-based explainability so risk-tier explanations can go beyond the coarse bucket shown today.
* Explore LightGBM / CatBoost as additional classical challengers.
* Extend the cost matrix to vary by loan amount rather than a single flat FN/FP cost.
* Package `prediction_engine.py` behind a lightweight API for programmatic (non-Streamlit) scoring.
* Add more languages and accessibility passes to the client-facing app.
* Set up CI to re-run the notebook pipeline and flag metric drift automatically.

## ⚠️ Disclaimer

This project was built for educational purposes as part of a TechTrek internship. Risk tiers and probabilities are model estimates on a public benchmark dataset, not a real underwriting decision, and should not be used as one.
