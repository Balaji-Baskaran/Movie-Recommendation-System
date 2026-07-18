# Movie Recommendation System

A Flask + Uvicorn web app that recommends Indian movies using a pre-trained model.

> The dataset is excluded from GitHub. Download it separately and keep it in a local `dataset/` folder.

## Features

- Movie search and recommendation engine
- Filter by genre, year, and industry
- Plotly-powered visualization
- Flask + ASGI deployment with `uvicorn`

## Project structure

- `app.py` - main web application
- `frontend/templates/` - HTML templates
- `frontend/static/` - CSS and static assets
- `libs/data_utils.py` - model loading and data helpers
- `module/recommender.py` - recommendation engine
- `views/` - chart and icon utilities
- `notebook/movie_recommendation.ipynb` - training and exploration notebook

## Requirements

- Python 3.9+
- Flask
- Uvicorn
- asgiref
- pandas
- numpy
- scikit-learn
- plotly
- joblib

Install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Local dataset and model files

This repository intentionally does not include the dataset or the trained model file.

1. Download the dataset file `indian_movies.csv` from the dataset source (for example, Kaggle).
2. Create a local folder named `dataset/` in the repository root.
3. Place the dataset file here:

```text
dataset/indian_movies.csv
```

4. Create a local folder named `model/`.
5. Place the trained model file here:

```text
model/movie_recommendation_model.pkl
```

If the model file is missing, use `notebook/movie_recommendation.ipynb` to train or generate it locally.

## Run the app

```bash
uvicorn app:asgi_app --reload --port 8000
```

Open your browser:

```text
http://localhost:8000/
```

