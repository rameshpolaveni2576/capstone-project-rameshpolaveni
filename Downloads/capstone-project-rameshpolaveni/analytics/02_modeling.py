from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

matplotlib.use("Agg")

DATA_PATH = Path(__file__).resolve().parent / "titanic.csv"
OUTPUT_DIR = Path(__file__).resolve().parent


def build_preprocessor(numeric_features: list[str] | None = None, categorical_features: list[str] | None = None) -> ColumnTransformer:
    if numeric_features is None:
        numeric_features = ["age", "sibsp", "parch", "fare"]
    if categorical_features is None:
        categorical_features = ["sex", "embarked"]
    return ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]),
                numeric_features,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]),
                categorical_features,
            ),
        ]
    )


def evaluate_classifier(y_true, y_pred, y_proba) -> dict:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_proba),
    }


def plot_roc_curve(models: dict[str, Pipeline], X_test: pd.DataFrame, y_test: pd.Series) -> None:
    plt.figure(figsize=(7, 5))
    for name, model in models.items():
        proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, proba)
        plt.plot(fpr, tpr, label=f"{name} (AUC={roc_auc_score(y_test, proba):.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Baseline")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("ROC curves for Titanic classifiers")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "roc_curve.png", dpi=150)
    plt.close()


def save_model_summary(results_df: pd.DataFrame, output_path: Path) -> None:
    results_df.to_csv(output_path, index=False)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["survived", "name", "ticket", "embark_town", "who", "adult_male", "alone", "alive"], errors="ignore")
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Class balance in target:")
    print(y.value_counts(normalize=True))
    print("\nReasoning: stratification preserves the 0/1 survival rate in both train and test sets, preventing a biased split where one class could be underrepresented in evaluation.")

    models = {
        "Logistic Regression": Pipeline([
            ("preprocessor", build_preprocessor()),
            ("model", LogisticRegression(max_iter=2000, random_state=42)),
        ]),
        "Decision Tree": Pipeline([
            ("preprocessor", build_preprocessor()),
            ("model", DecisionTreeClassifier(random_state=42, max_depth=4)),
        ]),
        "Random Forest": Pipeline([
            ("preprocessor", build_preprocessor()),
            ("model", RandomForestClassifier(n_estimators=300, random_state=42)),
        ]),
    }

    comparison_rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        metrics = evaluate_classifier(y_test, y_pred, y_prob)
        metrics["model"] = name
        comparison_rows.append(metrics)

        cm = confusion_matrix(y_test, y_pred)
        print(f"\n=== {name} ===")
        print(cm)
        print(classification_report(y_test, y_pred, target_names=["Not Survived", "Survived"]))
        print(metrics)

        if name == "Decision Tree":
            fitted_tree = model.named_steps["model"]
            feature_names = model.named_steps["preprocessor"].get_feature_names_out()
            fig, ax = plt.subplots(figsize=(16, 10))
            plot_tree(fitted_tree, feature_names=feature_names, class_names=["No", "Yes"], filled=True, rounded=True, ax=ax)
            plt.tight_layout()
            plt.savefig(OUTPUT_DIR / "decision_tree.png", dpi=150)
            plt.close(fig)

    comparison_df = pd.DataFrame(comparison_rows)
    comparison_df = comparison_df[["model", "accuracy", "precision", "recall", "f1", "roc_auc"]]
    print("\nModel comparison table:")
    print(comparison_df.to_string(index=False))
    save_model_summary(comparison_df, OUTPUT_DIR / "classifier_comparison.csv")

    # ROC curves
    plot_roc_curve({name: model for name, model in models.items()}, X_test, y_test)

    # Imbalance handling comparison using logistic regression
    imbalance_results = []
    preprocessor = build_preprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    base_model = LogisticRegression(max_iter=2000, random_state=42)
    w_model = LogisticRegression(max_iter=2000, random_state=42, class_weight="balanced")
    base_model.fit(X_train_proc, y_train)
    w_model.fit(X_train_proc, y_train)

    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_proc, y_train)
    smote_model = LogisticRegression(max_iter=2000, random_state=42)
    smote_model.fit(X_train_smote, y_train_smote)

    for label, model, test_x, test_y in [
        ("baseline", base_model, X_test_proc, y_test),
        ("class_weight_balanced", w_model, X_test_proc, y_test),
        ("smote", smote_model, X_test_proc, y_test),
    ]:
        pred = model.predict(test_x)
        prob = model.predict_proba(test_x)[:, 1]
        metrics = evaluate_classifier(test_y, pred, prob)
        metrics["variant"] = label
        imbalance_results.append(metrics)

    imbalance_df = pd.DataFrame(imbalance_results)
    print("\nImbalance handling comparison:")
    print(imbalance_df[["variant", "precision", "recall", "f1", "roc_auc"]].to_string(index=False))

    # Hyperparameter tuning for Random Forest with OOB score.
    # Fit preprocessing on the training set only, then tune the forest on the transformed matrix.
    rf_preprocessor = build_preprocessor()
    X_train_rf = rf_preprocessor.fit_transform(X_train)
    rf_estimator = RandomForestClassifier(oob_score=True, random_state=42, n_jobs=-1)
    rf_search = GridSearchCV(
        estimator=rf_estimator,
        param_grid={
            "n_estimators": [100, 200],
            "max_depth": [None, 5, 10],
            "max_features": ["sqrt", "log2", 1.0],
        },
        cv=3,
        scoring="f1",
        n_jobs=1,
    )
    rf_search.fit(X_train_rf, y_train)
    print("\nRandom forest best params:", rf_search.best_params_)
    print("Random forest OOB score:", rf_search.best_estimator_.oob_score_)
    models["Random Forest"] = Pipeline([
        ("preprocessor", rf_preprocessor),
        ("model", rf_search.best_estimator_),
    ])

    # Regression side-task: predict fare from all other available features
    regress_X = df.drop(columns=["fare"], errors="ignore")
    regress_y = df["fare"]
    reg_X_train, reg_X_test, reg_y_train, reg_y_test = train_test_split(
        regress_X, regress_y, test_size=0.2, random_state=42
    )
    regression_numeric = [col for col in reg_X_train.select_dtypes(include=["number"]).columns if col != "fare"]
    regression_categorical = [col for col in reg_X_train.select_dtypes(exclude=["number"]).columns if col not in ["name", "ticket", "embark_town", "who", "alive"]]
    reg_preprocessor = build_preprocessor(regression_numeric, regression_categorical)
    reg_pipeline = Pipeline([
        ("preprocessor", reg_preprocessor),
        ("model", LinearRegression()),
    ])
    reg_pipeline.fit(reg_X_train, reg_y_train)
    reg_pred = reg_pipeline.predict(reg_X_test)
    reg_mae = mean_absolute_error(reg_y_test, reg_pred)
    reg_rmse = mean_squared_error(reg_y_test, reg_pred, squared=False)
    reg_r2 = r2_score(reg_y_test, reg_pred)
    n = len(reg_y_test)
    p = reg_X_test.shape[1]
    adj_r2 = 1 - (1 - reg_r2) * (n - 1) / (n - p - 1)
    print("\nRegression metrics:")
    print({"MAE": reg_mae, "RMSE": reg_rmse, "R2": reg_r2, "Adjusted_R2": adj_r2})

    residuals = reg_y_test - reg_pred
    plt.figure(figsize=(8, 5))
    plt.scatter(reg_pred, residuals)
    plt.axhline(0, color="red", linestyle="--")
    plt.title("Residual plot for fare prediction")
    plt.xlabel("Predicted fare")
    plt.ylabel("Residual")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fare_residuals.png", dpi=150)
    plt.close()

    # Final recommendation text
    best_classifier = comparison_df.sort_values("f1", ascending=False).iloc[0]["model"]
    best_metrics = comparison_df.sort_values("f1", ascending=False).iloc[0]
    rec_text = (
        f"I would deploy the {best_classifier} classifier for the Titanic survival task because it achieved the strongest overall balance of metrics, with accuracy {best_metrics['accuracy']:.3f}, precision {best_metrics['precision']:.3f}, recall {best_metrics['recall']:.3f}, F1 {best_metrics['f1']:.3f}, and ROC-AUC {best_metrics['roc_auc']:.3f}. The model also keeps a strong classification boundary for both surviving and non-surviving passengers without sacrificing recall. In contrast, the other models are competitive but do not outperform this configuration on the same held-out split. For this business use case, the chosen model preserves both operational recall and robust discrimination, which is the safer trade-off for a high-stakes downstream decision."
    )
    print("\nFinal recommendation:")
    print(rec_text)
    (OUTPUT_DIR / "final_recommendation.txt").write_text(rec_text, encoding="utf-8")

    # Save best full pipeline as a single object
    best_name = best_classifier
    best_pipeline = models[best_name]
    joblib.dump(best_pipeline, OUTPUT_DIR / "best_titanic_pipeline.joblib")
    loaded = joblib.load(OUTPUT_DIR / "best_titanic_pipeline.joblib")
    raw_example = X_test.iloc[[0]].copy()
    original_pred = best_pipeline.predict(raw_example)
    restored_pred = loaded.predict(raw_example)
    print("\nReloaded pipeline validation:", np.array_equal(original_pred, restored_pred))

    print("\nModeling pipeline complete. Outputs saved under analytics/.")


if __name__ == "__main__":
    main()
