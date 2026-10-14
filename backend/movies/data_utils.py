import joblib
import numpy as np
import pandas as pd

_model_cache = {}

def load_model(model_path="model/movie_recommendation_model.pkl"):
    if model_path not in _model_cache:
        _model_cache[model_path] = joblib.load(model_path)
    return _model_cache[model_path]

def prepare_data(raw):
    df = raw["dataframe"].copy()
    emb = raw["embeddings"].astype(np.float32)
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return df, emb / norms
