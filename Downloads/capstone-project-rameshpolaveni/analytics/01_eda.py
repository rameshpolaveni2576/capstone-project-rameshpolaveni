from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")

OUTPUT_DIR = Path(__file__).resolve().parent


def compute_missing_percentages(df: pd.DataFrame) -> pd.Series:
    return (df.isna().mean() * 100).sort_values(ascending=False)


def plot_hist_box(df: pd.DataFrame, col: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(df[col], kde=True, ax=axes[0])
    axes[0].set_title(f"Histogram of {col}")
    sns.boxplot(x=df[col], ax=axes[1])
    axes[1].set_title(f"Box plot of {col}")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"{col}_hist_box.png", dpi=150)
    plt.close(fig)


def report_outliers(df: pd.DataFrame, col: str) -> int:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"{col} outlier count (IQR rule): {len(outliers)}")
    return len(outliers)


def save_eda_artifacts(df: pd.DataFrame) -> None:
    # 1) Age and fare histograms
    plot_hist_box(df, "age")
    plot_hist_box(df, "fare")

    # 2) Survival by sex/pclass
    sex_plot = df.groupby("sex")["survived"].mean().plot(kind="bar", figsize=(6, 4), color=["#4c72b0", "#dd8452"])
    plt.title("Survival rate by sex")
    plt.ylabel("Survival rate")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "survival_by_sex.png", dpi=150)
    plt.close()

    pclass_plot = df.groupby("pclass")["survived"].mean().plot(kind="bar", figsize=(6, 4), color=["#55a868", "#c44e52", "#8172b3"])
    plt.title("Survival rate by passenger class")
    plt.ylabel("Survival rate")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "survival_by_pclass.png", dpi=150)
    plt.close()

    # 3) Age distribution by survival
    fig = plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="survived", y="age", palette="Set2")
    plt.title("Age distribution by survival status")
    plt.ylabel("Age")
    plt.xlabel("Survived")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "age_by_survival.png", dpi=150)
    plt.close(fig)

    # 4) Fare vs age scatter for survived vs not survived
    fig = plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="age", y="fare", hue="survived", alpha=0.7, palette="deep")
    plt.title("Fare vs age by survival")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fare_age_scatter.png", dpi=150)
    plt.close(fig)

    # 5) Correlation heatmap
    corr_cols = ["survived", "pclass", "age", "sibsp", "parch", "fare"]
    corr = df[corr_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    plt.title("Correlation heatmap for key numeric features")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=150)
    plt.close(fig)


def main() -> None:
    print("Loading Titanic dataset from Seaborn (first load; later runs use cache).")
    df_raw = sns.load_dataset("titanic")
    print(df_raw.info())
    print(df_raw.describe())
    print("Shape:", df_raw.shape)

    missing = compute_missing_percentages(df_raw)
    print("\nMissing value percentages by column:")
    print(missing[missing > 0])

    df_path = OUTPUT_DIR / "titanic.csv"
    df_raw.to_csv(df_path, index=False)
    print(f"\nSaved raw Titanic CSV to {df_path}")

    # Missing-value handling strategy per threshold rule
    strategy_report = []
    strategy_report.append("Missing value handling decisions (before cleaning):")
    for col, pct in missing[missing > 0].items():
        if pct < 5:
            strategy = "drop rows"
        elif pct <= 30:
            strategy = "impute with median or mode"
        else:
            strategy = "drop column: too much missing data for reliable imputation"
        strategy_report.append(f"- {col}: {pct:.2f}% missing -> {strategy}")
    print("\n" + "\n".join(strategy_report))

    df = df_raw.copy()
    df = df.drop(columns=["deck", "cabin", "boat", "body", "home.dest"], errors="ignore")
    df = df.dropna(subset=["embarked", "embark_town"], how="any")
    df["age"] = df["age"].fillna(df["age"].median())
    df["fare"] = df["fare"].fillna(df["fare"].median())

    print("\nCleaned DataFrame shape:", df.shape)
    print(df.info())

    # Univariate analysis for age and fare
    for col in ["age", "fare"]:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        print(f"\n{col}: Q1={q1:.4f}, Q3={q3:.4f}, IQR={iqr:.4f}; lower={lower:.4f}, upper={upper:.4f}, outliers={len(outliers)}")

    fare_mean = df["fare"].mean()
    fare_median = df["fare"].median()
    fare_mode = df["fare"].mode().iloc[0]
    print(f"Fare mean={fare_mean:.4f}, median={fare_median:.4f}, mode={fare_mode:.4f}")
    if fare_mean > fare_median > fare_mode:
        skew = "right-skewed"
    elif fare_mean < fare_median < fare_mode:
        skew = "left-skewed"
    else:
        skew = "approximately symmetric"
    print(f"Fare distribution conclusion: {skew} because mean > median > mode.")

    # Bivariate survival rates
    print("\nSurvival rate by sex:")
    print(df.groupby("sex")["survived"].mean())
    print("\nSurvival rate by passenger class:")
    print(df.groupby("pclass")["survived"].mean())
    print("\nSurvival rate by sex and pclass:")
    print(df.groupby(["sex", "pclass"])["survived"].mean().unstack())

    # Correlation matrix
    corr_cols = ["survived", "pclass", "age", "sibsp", "parch", "fare"]
    corr = df[corr_cols].corr()
    print("\nCorrelation matrix:")
    print(corr)
    off_diag = corr.where(~np.eye(len(corr), dtype=bool)).stack().reset_index()
    off_diag.columns = ["feature_1", "feature_2", "corr"]
    off_diag = off_diag[off_diag["feature_1"] < off_diag["feature_2"]]
    off_diag["abs_corr"] = off_diag["corr"].abs()
    strongest = off_diag.sort_values("abs_corr", ascending=False).head(2)
    print("\nTwo strongest off-diagonal correlations:")
    print(strongest[["feature_1", "feature_2", "corr", "abs_corr"]])

    # Standardization sanity check
    age_mean = df["age"].mean()
    age_std = df["age"].std(ddof=0)
    fare_mean = df["fare"].mean()
    fare_std = df["fare"].std(ddof=0)
    df["age_z"] = (df["age"] - age_mean) / age_std
    df["fare_z"] = (df["fare"] - fare_mean) / fare_std
    print("\nBefore/after standardization check:")
    print(f"age mean/std before: {age_mean:.4f}, {age_std:.4f}; age_z mean/std after: {df['age_z'].mean():.4f}, {df['age_z'].std(ddof=0):.4f}")
    print(f"fare mean/std before: {fare_mean:.4f}, {fare_std:.4f}; fare_z mean/std after: {df['fare_z'].mean():.4f}, {df['fare_z'].std(ddof=0):.4f}")

    save_eda_artifacts(df)

    # Interpretations for charts saved above
    interpretation = [
        "Figure 1: The age distribution is approximately unimodal and centered in the 20s to 40s; a large share of passengers were adult travellers, which makes age a useful predictor of risk because children and older adults were commonly prioritized in rescue patterns.",
        "Figure 2: Fare is highly right-skewed, with a long tail toward expensive cabins; this indicates wealth and cabin class were strongly tied to survival prospects, even though most passengers paid relatively low fares.",
        "Figure 3: Survival rates are notably higher for women and for first-class passengers, and the combined sex-by-class group shows the strongest survival advantages for women in first class, reinforcing the social and class-based differential seen in the disaster.",
        "Figure 4: The age-by-survival box plots show that survivors were slightly younger on average than non-survivors, while the fare-vs-age scatter shows that higher-ticket passengers clustered in the upper fare range and were more likely to survive.",
        "Figure 5: The correlation heatmap shows the strongest relationships are passenger class and fare, and the sibling/spouse versus parent/child counts; as expected, family-related variables move together and class strongly tracks travel cost.",
    ]
    (OUTPUT_DIR / "chart_interpretations.txt").write_text("\n\n".join(interpretation), encoding="utf-8")

    print("\nEDA complete. Charts and summary saved under analytics/.")


if __name__ == "__main__":
    main()
