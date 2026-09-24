"""
Prediction engine for the AI Credit Risk & Loan Default Intelligence Platform.

This module is intentionally UI-agnostic: it only loads saved artifacts and runs
inference. It never retrains, tunes, recalibrates, or otherwise modifies any model,
preprocessing step, threshold, or calibration - it only reuses what earlier notebooks
already produced and saved to disk.

Design note on missing features
--------------------------------
The applicant-facing form only asks for a practical subset of the model's full feature
schema (see PRACTICAL_FIELD_MAP below) - not all ~586 raw model features. Any expected
feature the form does not collect is left as NaN in the row handed to the saved
pipeline. This is a safe, well-defined strategy specifically *because* every saved
preprocessing pipeline in this project already imputes missing values itself (median
for numeric columns, a constant "missing" category for categorical columns - see
01_eda.ipynb / 03_ml_experiments.ipynb). An unfilled field is therefore handled exactly
the same way the training pipeline already handles a real applicant with missing data
in that column - nothing is invented here, and neither the model nor the preprocessing
artifact is touched.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import joblib
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Practical, applicant-facing fields the GUI actually collects, and how each one
# maps onto the model's real feature schema. This is the ONLY place that encodes
# assumptions about specific column names - if a project's real feature list uses
# different names, only this map needs editing.
#
# Each entry: practical_field -> (model_feature_name, transform_fn or None)
# transform_fn takes the raw form value and returns the value to place in that
# model column (e.g. age in years -> DAYS_BIRTH as a negative day-count).
# ---------------------------------------------------------------------------
PRACTICAL_FIELD_MAP: dict[str, tuple[str, Any]] = {
    "age_years": ("DAYS_BIRTH", lambda v: -int(round(v * 365.25))),
    "years_employed": ("DAYS_EMPLOYED", lambda v: -int(round(v * 365.25)) if v is not None else None),
    "annual_income": ("AMT_INCOME_TOTAL", lambda v: float(v)),
    "loan_amount": ("AMT_CREDIT", lambda v: float(v)),
    "annuity_amount": ("AMT_ANNUITY", lambda v: float(v)),
    "goods_price": ("AMT_GOODS_PRICE", lambda v: float(v)),
    "num_children": ("CNT_CHILDREN", lambda v: int(v)),
    "has_bureau_history": ("HAS_BUREAU_HISTORY", lambda v: int(v)),
    "has_previous_application": ("HAS_PREVIOUS_APPLICATION", lambda v: int(v)),
    "gender": ("CODE_GENDER", lambda v: v),
    "education": ("NAME_EDUCATION_TYPE", lambda v: v),
    "family_status": ("NAME_FAMILY_STATUS", lambda v: v),
    "contract_type": ("NAME_CONTRACT_TYPE", lambda v: v),
    "owns_car": ("FLAG_OWN_CAR", lambda v: "Y" if v else "N"),
    "owns_realty": ("FLAG_OWN_REALTY", lambda v: "Y" if v else "N"),
    "occupation": ("OCCUPATION_TYPE", lambda v: v),
}


@dataclass
class LoadedArtifacts:
    feature_lists: dict
    classical_model: Any
    classical_metadata: dict
    mlp_model: Any | None
    mlp_preprocessor: Any | None
    mlp_calibrator: Any | None
    mlp_metadata: dict | None
    comparison_table: pd.DataFrame | None


class ArtifactLoadError(RuntimeError):
    """Raised when a required saved artifact is missing or fails to load."""


def _read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_artifacts(project_root: str) -> LoadedArtifacts:
    """Load all saved artifacts required by the application."""

    reports_dir = os.path.join(project_root, "reports")
    models_dir = os.path.join(project_root, "models", "versioned_artifacts")

    feature_list_path = os.path.join(
        reports_dir, "final_ml_feature_list.json"
    )
    classical_model_path = os.path.join(
        models_dir, "best_classical_model.joblib"
    )
    classical_meta_path = os.path.join(
        reports_dir, "final_model_metadata.json"
    )

    for required_path, label in [
        (feature_list_path, "final_ml_feature_list.json"),
        (classical_model_path, "best_classical_model.joblib"),
        (classical_meta_path, "final_model_metadata.json"),
    ]:
        if not os.path.exists(required_path):
            raise ArtifactLoadError(
                f"Required artifact not found: {label}\n"
                f"Expected at: {required_path}"
            )

    feature_lists = _read_json(feature_list_path)

    # --------------------------------------------------------
    # Classical Champion
    # --------------------------------------------------------
    classical_bundle = joblib.load(classical_model_path)
    classical_metadata = _read_json(classical_meta_path)

    if isinstance(classical_bundle, dict):
        classical_model = classical_bundle.get(
            "pipeline",
            classical_bundle.get("model")
        )

        classical_calibrator = classical_bundle.get("calibrator")
        classical_calibration_method = classical_bundle.get(
            "calibration_method"
        )

        classical_threshold = classical_bundle.get(
            "decision_threshold",
            classical_bundle.get("threshold")
        )

        classical_metadata = {
            **classical_metadata,
            "calibrator": classical_calibrator,
            "calibration_method": classical_calibration_method,
            "decision_threshold": classical_threshold,
        }

    else:
        classical_model = classical_bundle

    # --------------------------------------------------------
    # MLP
    # --------------------------------------------------------
    mlp_model = None
    mlp_preprocessor = None
    mlp_calibrator = None
    mlp_metadata = None

    mlp_model_path = os.path.join(
        models_dir, "best_mlp_model.keras"
    )
    mlp_preproc_path = os.path.join(
        models_dir, "mlp_preprocessing_pipeline.joblib"
    )
    mlp_calib_path = os.path.join(
        models_dir, "mlp_calibrator.joblib"
    )

    # Correct filename saved by DL notebook
    mlp_meta_path = os.path.join(
        reports_dir, "dl_model_metadata.json"
    )

    if all(
        os.path.exists(p)
        for p in [
            mlp_model_path,
            mlp_preproc_path,
            mlp_calib_path,
            mlp_meta_path,
        ]
    ):
        try:
            import tensorflow as tf

            mlp_model = tf.keras.models.load_model(
                mlp_model_path
            )

            mlp_preprocessor = joblib.load(
                mlp_preproc_path
            )

            mlp_calibrator = joblib.load(
                mlp_calib_path
            )

            mlp_metadata = _read_json(
                mlp_meta_path
            )

        except Exception:
            mlp_model = None
            mlp_preprocessor = None
            mlp_calibrator = None
            mlp_metadata = None

    # --------------------------------------------------------
    # Comparison table
    # --------------------------------------------------------
    comparison_table = None

    comparison_path = os.path.join(
        reports_dir,
        "model_comparison_cv_results.csv"
    )

    if os.path.exists(comparison_path):
        try:
            comparison_table = pd.read_csv(
                comparison_path
            )
        except Exception:
            comparison_table = None

    return LoadedArtifacts(
        feature_lists=feature_lists,
        classical_model=classical_model,
        classical_metadata=classical_metadata,
        mlp_model=mlp_model,
        mlp_preprocessor=mlp_preprocessor,
        mlp_calibrator=mlp_calibrator,
        mlp_metadata=mlp_metadata,
        comparison_table=comparison_table,
    )


def build_full_feature_row(form_values: dict, all_features: list[str]) -> pd.DataFrame:
    """Turn the practical form values into a single-row DataFrame with every column
    the saved pipeline expects. Fields the form didn't collect (or the user left
    blank) become NaN - handled downstream by the saved pipeline's own imputers.
    """
    row = {feature: np.nan for feature in all_features}

    for form_key, (model_column, transform_fn) in PRACTICAL_FIELD_MAP.items():
        if model_column not in row:
            continue  # this project's real schema doesn't use this column - skip safely
        raw_value = form_values.get(form_key)
        if raw_value is None or raw_value == "":
            continue  # left blank -> stays NaN -> imputed by the saved pipeline
        try:
            row[model_column] = transform_fn(raw_value) if transform_fn else raw_value
        except Exception:
            row[model_column] = np.nan

    return pd.DataFrame([row], columns=all_features)


def predict_classical(
    artifacts: LoadedArtifacts,
    feature_row: pd.DataFrame
) -> dict:
    """Run the saved Classical Champion pipeline."""

    raw_proba = float(
        artifacts.classical_model
        .predict_proba(feature_row)[:, 1][0]
    )

    calibrator = artifacts.classical_metadata.get(
        "calibrator"
    )

    calibration_method = artifacts.classical_metadata.get(
        "calibration_method"
    )

    if calibrator is not None:

        if calibration_method == "isotonic":
            proba = float(
                calibrator.predict(
                    np.array([raw_proba])
                )[0]
            )

        else:
            proba = float(
                calibrator.predict_proba(
                    np.array([[raw_proba]])
                )[:, 1][0]
            )

    else:
        proba = raw_proba

    # Keep the calibrated output within the mathematical probability range.
    # This does not alter the saved model or calibration artifact.
    proba = float(np.clip(proba, 0.0, 1.0))

    threshold = float(
        artifacts.classical_metadata.get(
            "decision_threshold",
            0.5
        )
    )

    return {
        "model_name": artifacts.classical_metadata.get(
            "model_type",
            "Logistic Regression"
        ),
        "probability": proba,
        "threshold": threshold,
        "decision": (
            "REVIEW"
            if proba >= threshold
            else "APPROVE"
        ),
    }


def predict_mlp(
    artifacts: LoadedArtifacts,
    feature_row: pd.DataFrame
) -> dict | None:
    """Run the saved MLP prediction pipeline."""

    if artifacts.mlp_model is None:
        return None

    transformed = (
        artifacts.mlp_preprocessor
        .transform(feature_row)
        .astype("float32")
    )

    raw_score = (
        artifacts.mlp_model
        .predict(
            transformed,
            verbose=0
        )
        .ravel()
    )

    calibrator_bundle = artifacts.mlp_calibrator

    method = calibrator_bundle["method"]
    calibrator = calibrator_bundle["calibrator"]

    if method == "isotonic":
        calibrated = calibrator.predict(raw_score)
    else:
        calibrated = calibrator.predict_proba(
            raw_score.reshape(-1, 1)
        )[:, 1]

    proba = float(
        np.asarray(calibrated).ravel()[0]
    )

    threshold = float(
        artifacts.mlp_metadata.get(
            "decision_threshold",
            0.5
        )
    )

    return {
        "model_name": "MLP",
        "probability": proba,
        "threshold": threshold,
        "decision": (
            "REVIEW"
            if proba >= threshold
            else "APPROVE"
        ),
    }

def risk_tier(probability: float) -> tuple[str, str]:
    """Map a calibrated probability to a human-readable risk tier and a semantic
    color key (resolved to an actual color by the UI layer's theme).
    Bands are intentionally coarse and documented, not a precision instrument.
    """
    if probability < 0.05:
        return "LOW RISK", "success"
    if probability < 0.15:
        return "MODERATE RISK", "caution"
    if probability < 0.30:
        return "HIGH RISK", "warning"
    return "VERY HIGH RISK", "danger"