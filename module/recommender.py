import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend(movie_idx, df, emb_norm, n=10):
    scores = cosine_similarity(emb_norm[movie_idx:movie_idx+1], emb_norm)[0]
    scores[movie_idx] = -1
    top_idx = np.argsort(scores)[::-1][:n]
    results = []
    for rank, idx in enumerate(top_idx, 1):
        row = df.iloc[idx]
        results.append({
            "rank": rank,
            "idx": int(idx),
            "score": float(scores[idx]),
            "title": row["title"],
            "industry": row["industry"],
            "genre_list": row["genre_list"] if isinstance(row["genre_list"], list) else [],
            "overview": str(row["overview"]) if pd.notna(row["overview"]) else "",
            "rating": float(row["rating"]) if pd.notna(row["rating"]) else 0.0,
            "popularity": float(row["popularity"]) if pd.notna(row["popularity"]) else 0.0,
            "poster_path": str(row["poster_path"]) if pd.notna(row["poster_path"]) else "",
            "year": int(row["year"]) if pd.notna(row["year"]) else 0,
        })
    return results