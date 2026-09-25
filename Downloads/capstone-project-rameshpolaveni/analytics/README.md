# Analytics Module

## Goal

This module follows the project brief for an end-to-end Titanic analytics pipeline: load the dataset once, clean and profile it, save an offline fallback CSV, visualize the main story, and then build and evaluate a predictive modeling pipeline.

## Run

```bash
python analytics/02_modeling.py
```

This script reads the saved fallback dataset at `analytics/titanic.csv`, populates the EDA and model outputs, and saves the final fitted pipeline artifact at `analytics/best_titanic_pipeline.joblib`.

## Data flow

1. The Titanic dataset is loaded once from Seaborn if available, then saved locally as `analytics/titanic.csv`.
2. The cleaned data is used for profiling, missing-value handling, visual storytelling, and z-score sanity checks.
3. The modeling stage performs a stratified train/test split, preprocesses numerical and categorical features using train-only fitting, evaluates Logistic Regression, Decision Tree, and Random Forest, and runs an imbalance comparison plus a RandomForest tuning step.
4. A regression side-task predicts `fare`, and a final recommendation summary is written to `analytics/final_recommendation.txt`.

## Key outputs

- `analytics/titanic.csv` — committed offline fallback dataset
- `analytics/classifier_comparison.csv` — side-by-side model metrics
- `analytics/decision_tree.png` — tree visualization
- `analytics/roc_curve.png` — ROC curves for all classifiers
- `analytics/fare_residuals.png` — residual plot for the regression task
- `analytics/best_titanic_pipeline.joblib` — saved end-to-end fitted pipeline

## Design summary

This workflow keeps the full lifecycle in one connected story: one data load, one cleaned dataset, one modeling pass, and a final pipeline artifact that can be re-used on raw input after reloading with `joblib.load(...)`.
