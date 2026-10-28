import os
import sys
import pickle

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(PROJECT_ROOT)

from src.preprocessing import (
    load_data,
    prepare_training_data
)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "climate_skin_data.csv"
)

MODEL_DIRECTORY = os.path.join(
    PROJECT_ROOT,
    "models"
)

os.makedirs(MODEL_DIRECTORY, exist_ok=True)

print("=" * 70)
print("LUMINA AI - MODEL TRAINING")
print("=" * 70)

df = load_data(DATA_PATH)

print(f"\nDataset shape: {df.shape}")

X, y, feature_columns = prepare_training_data(df)

print(f"Number of features: {len(feature_columns)}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}

results = []
trained_models = {}

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

for model_name, model in models.items():

    print(f"\nTraining {model_name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    results.append({
        "model": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })

    trained_models[model_name] = model

    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R2   : {r2:.4f}")

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="MAE"
)

print("\n" + "=" * 70)
print("FINAL MODEL COMPARISON")
print("=" * 70)

print(results_df.to_string(index=False))

best_model_name = results_df.iloc[0]["model"]
best_model = trained_models[best_model_name]

print(f"\nBest model: {best_model_name}")

model_path = os.path.join(
    MODEL_DIRECTORY,
    "skin_stress_model.pkl"
)

with open(model_path, "wb") as file:
    pickle.dump(best_model, file)

metadata = {
    "model_name": best_model_name,
    "feature_columns": feature_columns,
    "target": "stress_score"
}

metadata_path = os.path.join(
    MODEL_DIRECTORY,
    "model_metadata.pkl"
)

with open(metadata_path, "wb") as file:
    pickle.dump(metadata, file)

results_path = os.path.join(
    MODEL_DIRECTORY,
    "model_results.csv"
)

results_df.to_csv(
    results_path,
    index=False
)

if hasattr(best_model, "feature_importances_"):

    importance_df = pd.DataFrame({
        "feature": feature_columns,
        "importance": best_model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
    )

    importance_path = os.path.join(
        MODEL_DIRECTORY,
        "feature_importance.csv"
    )

    importance_df.to_csv(
        importance_path,
        index=False
    )

print("\nTraining completed.")
print(f"Model saved: {model_path}")
print(f"Metadata saved: {metadata_path}")
print(f"Results saved: {results_path}")