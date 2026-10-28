import pandas as pd

NUMERIC_FEATURES = [
    "uv_index",
    "pm25",
    "temperature",
    "humidity",
    "outdoor_hours",
    "age"
]

CATEGORICAL_FEATURES = [
    "skin_type",
    "activity_level"
]

TARGET_COLUMNS = [
    "stress_score",
    "stress_category"
]


def load_data(path):
    return pd.read_csv(path)


def prepare_features(df):
    data = df.copy()

    data = pd.get_dummies(
        data,
        columns=CATEGORICAL_FEATURES,
        dtype=int
    )

    return data


def get_feature_columns(df):
    return [
        column
        for column in df.columns
        if column not in TARGET_COLUMNS
    ]


def prepare_training_data(df):
    processed_data = prepare_features(df)

    feature_columns = get_feature_columns(
        processed_data
    )

    X = processed_data[feature_columns]
    y = processed_data["stress_score"]

    return X, y, feature_columns