from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def create_customer_dataset(n: int = 1800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    data = {
        "customer_id": np.arange(1, n + 1),
        "age": np.clip(rng.normal(38, 12, n), 18, 80).astype(int),
        "tenure_months": np.clip(rng.integers(1, 48, size=n), 1, 47),
        "monthly_income": np.clip(rng.lognormal(mean=3.8, sigma=0.55, size=n), 1000, 15000).round(2),
        "avg_order_value": np.clip(rng.normal(120, 45, n), 20, 500).round(2),
        "orders_last_6m": np.clip(rng.integers(1, 16, size=n), 1, 15),
        "days_since_last_order": np.clip(rng.gamma(shape=2.0, scale=18.0, size=n), 1, 120).astype(int),
        "support_tickets": np.clip(rng.poisson(0.8, n), 0, 10),
        "promo_click_rate": np.clip(rng.beta(2, 5, n), 0.01, 0.85).round(3),
        "satisfaction_score": np.clip(rng.normal(4.1, 0.8, n), 1, 5).round(2),
        "is_vip": rng.binomial(1, 0.18, n),
        "region": rng.choice(["North", "South", "East", "West"], size=n),
    }

    df = pd.DataFrame(data)
    score = (
        -1.4
        + 0.02 * df["age"]
        + 0.015 * df["days_since_last_order"]
        + 0.007 * df["support_tickets"]
        - 0.8 * df["is_vip"]
        - 0.5 * df["tenure_months"] / 12
        + 0.015 * df["avg_order_value"] / 10
        - 0.7 * df["promo_click_rate"]
    )
    df["churn"] = (rng.random(n) < sigmoid(score)).astype(int)
    return df


def save_summary(df: pd.DataFrame, output_dir: Path) -> None:
    summary = []
    summary.append("Zepto Customer Analytics Summary")
    summary.append("=" * 35)
    summary.append(f"Rows: {len(df)}")
    summary.append(f"Columns: {list(df.columns)}")
    summary.append("")
    summary.append("Churn rate: " + str(round(df['churn'].mean(), 4)))
    summary.append("Average order value: " + str(round(df['avg_order_value'].mean(), 2)))
    summary.append("Average days since last order: " + str(round(df['days_since_last_order'].mean(), 2)))
    summary.append("VIP share: " + str(round(df['is_vip'].mean(), 4)))
    summary.append("")
    summary.append(df.groupby("region")["churn"].mean().to_string())
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "eda_summary.txt").write_text("\n".join(summary), encoding="utf-8")


def train_and_evaluate(df: pd.DataFrame, output_dir: Path) -> None:
    X = df.drop(columns=["customer_id", "churn"])
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=250, random_state=42, class_weight="balanced")),
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    report = classification_report(y_test, y_pred)
    conf = confusion_matrix(y_test, y_pred)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "model_report.txt").write_text(
        f"Accuracy: {accuracy:.4f}\nAUC: {roc_auc:.4f}\n\nClassification report:\n{report}\n\nConfusion matrix:\n{conf}\n",
        encoding="utf-8",
    )
    joblib.dump(model, output_dir / "churn_model.joblib")

    print(f"Accuracy: {accuracy:.4f}")
    print(f"AUC: {roc_auc:.4f}")
    print(report)

    plt.figure(figsize=(8, 5))
    sns.heatmap(conf, annot=True, fmt="d", cmap="Blues", xticklabels=["No churn", "Churn"], yticklabels=["No churn", "Churn"])
    plt.title("Churn Prediction Confusion Matrix")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_matrix.png")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = create_customer_dataset()
    df.to_csv(DATA_DIR / "customer_churn.csv", index=False)
    save_summary(df, OUTPUT_DIR)
    train_and_evaluate(df, OUTPUT_DIR)

    print(f"Saved analytics dataset to: {DATA_DIR / 'customer_churn.csv'}")
    print(f"Saved outputs to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
