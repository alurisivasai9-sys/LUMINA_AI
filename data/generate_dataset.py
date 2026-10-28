import os
import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_SAMPLES = 5000


def categorize_stress(score):
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


def generate_dataset(n_samples=5000):
    np.random.seed(RANDOM_SEED)

    uv_index = np.random.uniform(0, 12, n_samples)

    pm25 = np.random.gamma(2.2, 25, n_samples)
    pm25 = np.clip(pm25, 5, 300)

    temperature = np.random.normal(30, 5, n_samples)
    temperature = np.clip(temperature, 15, 45)

    humidity = np.random.normal(65, 15, n_samples)
    humidity = np.clip(humidity, 20, 95)

    outdoor_hours = np.random.beta(2, 2, n_samples) * 10
    outdoor_hours = np.clip(outdoor_hours, 0, 10)

    age = np.random.randint(18, 29, n_samples)

    skin_type = np.random.choice(
        ["Dry", "Normal", "Oily", "Combination"],
        size=n_samples
    )

    activity_level = np.random.choice(
        ["Low", "Moderate", "High"],
        size=n_samples,
        p=[0.30, 0.45, 0.25]
    )

    uv_component = (uv_index / 12) * 30

    pollution_component = (
        np.clip(pm25, 0, 250) / 250
    ) * 25

    heat_component = (
        np.clip(temperature - 20, 0, 25) / 25
    ) * 15

    humidity_component = (
        np.abs(humidity - 60) / 40
    ) * 8

    outdoor_component = (
        outdoor_hours / 10
    ) * 15

    interaction_component = (
        (uv_index / 12)
        * (outdoor_hours / 10)
        * 8
    )

    skin_effect = np.select(
        [
            skin_type == "Dry",
            skin_type == "Normal",
            skin_type == "Oily",
            skin_type == "Combination"
        ],
        [5, 0, 1, 3],
        default=0
    )

    activity_effect = np.select(
        [
            activity_level == "Low",
            activity_level == "Moderate",
            activity_level == "High"
        ],
        [0, 2, 5],
        default=0
    )

    noise = np.random.normal(0, 3, n_samples)

    stress_score = (
        uv_component
        + pollution_component
        + heat_component
        + humidity_component
        + outdoor_component
        + interaction_component
        + skin_effect
        + activity_effect
        + noise
    )

    stress_score = np.clip(stress_score, 0, 100)

    stress_category = [
        categorize_stress(score)
        for score in stress_score
    ]

    dataset = pd.DataFrame({
        "uv_index": np.round(uv_index, 2),
        "pm25": np.round(pm25, 2),
        "temperature": np.round(temperature, 2),
        "humidity": np.round(humidity, 2),
        "outdoor_hours": np.round(outdoor_hours, 2),
        "age": age,
        "skin_type": skin_type,
        "activity_level": activity_level,
        "stress_score": np.round(stress_score, 2),
        "stress_category": stress_category
    })

    return dataset


def main():
    dataset = generate_dataset(N_SAMPLES)

    output_path = os.path.join(
        os.path.dirname(__file__),
        "climate_skin_data.csv"
    )

    dataset.to_csv(output_path, index=False)

    print("=" * 60)
    print("LUMINA AI DATASET GENERATED")
    print("=" * 60)
    print(f"Samples: {len(dataset)}")
    print(f"Columns: {len(dataset.columns)}")
    print(f"Saved to: {output_path}")
    print(dataset.head())
    print("\nStress category distribution:")
    print(dataset["stress_category"].value_counts())
    print("=" * 60)


if __name__ == "__main__":
    main()