import os
import sys

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "climate_skin_data.csv"
)

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("LUMINA AI - DATASET ANALYSIS")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)

print("\nFirst five rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDescriptive statistics:")
print(df.describe())

print("\nStress category distribution:")
print(df["stress_category"].value_counts())

numeric_columns = [
    "uv_index",
    "pm25",
    "temperature",
    "humidity",
    "outdoor_hours",
    "age",
    "stress_score"
]

correlation = df[numeric_columns].corr()

print("\nCorrelation with stress score:")
print(
    correlation["stress_score"]
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

plt.hist(
    df["stress_score"],
    bins=30
)

plt.title(
    "LUMINA AI - Stress Score Distribution"
)

plt.xlabel(
    "Environmental Skin Stress Score"
)

plt.ylabel(
    "Number of Samples"
)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

plt.scatter(
    df["uv_index"],
    df["stress_score"],
    alpha=0.3
)

plt.title(
    "UV Index vs Environmental Skin Stress"
)

plt.xlabel("UV Index")
plt.ylabel("Stress Score")

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

plt.scatter(
    df["pm25"],
    df["stress_score"],
    alpha=0.3
)

plt.title(
    "PM2.5 vs Environmental Skin Stress"
)

plt.xlabel("PM2.5")
plt.ylabel("Stress Score")

plt.tight_layout()
plt.show()

print("\nAnalysis completed.")
