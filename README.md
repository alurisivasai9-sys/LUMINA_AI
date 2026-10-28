# LUMINA AI

## Climate Skin Intelligence for India's Gen Z

LUMINA AI is a prototype designed for the L'Oréal Sustainability Challenge 2026.

The system estimates environmental skin stress using climate,
pollution, outdoor exposure, and user-profile factors.

## Core Inputs

- UV Index
- PM2.5
- Temperature
- Humidity
- Outdoor Exposure
- Age
- Skin Type
- Activity Level

## Machine Learning

The prototype compares:

- Linear Regression
- Random Forest Regression
- Gradient Boosting Regression

Evaluation metrics:

- MAE
- RMSE
- R²

## Run the Project

Generate the dataset:

```bash
python data/generate_dataset.py