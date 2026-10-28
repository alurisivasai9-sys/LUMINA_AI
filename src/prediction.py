import os
import joblib
import pandas as pd


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "skin_stress_model.pkl"
)

METADATA_PATH = os.path.join(
    BASE_DIR,
    "models",
    "model_metadata.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}\n\n"
            "Run: python src/train_model.py"
        )

    model = joblib.load(MODEL_PATH)

    metadata = {}

    if os.path.exists(METADATA_PATH):
        metadata = joblib.load(METADATA_PATH)

    return model, metadata


# ============================================================
# PREPARE INPUT
# ============================================================

def prepare_input(
    uv_index,
    pm25,
    temperature,
    humidity,
    outdoor_hours,
    age,
    skin_type,
    activity_level,
    feature_columns
):

    data = pd.DataFrame([
        {
            "uv_index": uv_index,
            "pm25": pm25,
            "temperature": temperature,
            "humidity": humidity,
            "outdoor_hours": outdoor_hours,
            "age": age,
            "skin_type": skin_type,
            "activity_level": activity_level
        }
    ])

    # One-hot encode categorical variables
    data = pd.get_dummies(
        data,
        columns=["skin_type", "activity_level"],
        dtype=int
    )

    # Make sure input contains exactly the same
    # columns used during model training.
    data = data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    return data


# ============================================================
# CATEGORY
# ============================================================

def get_stress_category(score):

    if score <= 20:
        return "Very Low"

    elif score <= 40:
        return "Low"

    elif score <= 60:
        return "Moderate"

    elif score <= 80:
        return "High"

    else:
        return "Very High"


# ============================================================
# MAIN PREDICTION FUNCTION
# ============================================================

def predict_stress(
    uv_index,
    pm25,
    temperature,
    humidity,
    outdoor_hours,
    age,
    skin_type,
    activity_level
):

    model, metadata = load_model()

    # Get feature columns saved during training
    feature_columns = metadata.get("feature_columns")

    # Fallback if metadata does not contain them
    if feature_columns is None:

        feature_columns = [
            "uv_index",
            "pm25",
            "temperature",
            "humidity",
            "outdoor_hours",
            "age"
        ]

        skin_types = [
            "skin_type_Dry",
            "skin_type_Normal",
            "skin_type_Oily",
            "skin_type_Combination"
        ]

        activities = [
            "activity_level_Low",
            "activity_level_Moderate",
            "activity_level_High"
        ]

        feature_columns.extend(skin_types)
        feature_columns.extend(activities)

    # Prepare user input
    X = prepare_input(
        uv_index=uv_index,
        pm25=pm25,
        temperature=temperature,
        humidity=humidity,
        outdoor_hours=outdoor_hours,
        age=age,
        skin_type=skin_type,
        activity_level=activity_level,
        feature_columns=feature_columns
    )

    # Predict
    prediction = model.predict(X)

    score = float(prediction[0])

    # Keep score between 0 and 100
    score = max(0.0, min(100.0, score))

    category = get_stress_category(score)

    return {
        "score": round(score, 1),
        "category": category
    }