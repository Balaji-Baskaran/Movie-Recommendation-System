import json
import logging
from pathlib import Path
import pandas as pd
from django.conf import settings

from .data_utils import load_model, prepare_data
from .recommender import recommend
from .chart_heartbeat import make_heartbeat_chart

logger = logging.getLogger("movies")


class MovieRecommenderService:
    _instance = None

    def __init__(self):
        model_path = Path(settings.BASE_DIR) / "model" / "movie_recommendation_model.pkl"
        if not model_path.exists():
            model_path = Path(settings.ROOT_DIR) / "model" / "movie_recommendation_model.pkl"
        logger.info(f"Loading recommendation model from {model_path}...")
        
        self._raw = load_model(str(model_path))
        self.df, self.emb_norm = prepare_data(self._raw)
        self.df["genre_set"] = self.df["genre_list"].apply(
            lambda x: set(g.lower() for g in x if g) if isinstance(x, list) else set()
        )
        logger.info(f"Model loaded │ {len(self.df)} movies in dataset")

        self.industries = sorted(self.df["industry"].dropna().unique().tolist())
        self.genres, self.years = self._get_filter_options()
        self.movie_options = self._build_movie_options()

        self.movie_options_json = json.dumps(self.movie_options)
        self.filter_options_json = json.dumps({
            "genres": self.genres,
            "years": self.years,
            "industries": self.industries,
        })

    def _get_filter_options(self):
        all_genres = set()
        for g_list in self.df["genre_list"].dropna():
            if isinstance(g_list, list):
                for g in g_list:
                    if g:
                        all_genres.add(g.strip().title())
        all_years = sorted(
            [int(y) for y in self.df["year"].dropna().unique() if y > 0],
            reverse=True,
        )
        return sorted(list(all_genres)), all_years

    def _build_movie_options(self):
        opts = []
        for idx, row in self.df.iterrows():
            year_val = int(row["year"]) if pd.notna(row.get("year")) else 0
            label = f"{row['title']}  ({year_val}  ·  {row['industry']})"
            opts.append({"idx": int(idx), "label": label})
        return opts

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MovieRecommenderService()
        return cls._instance


def get_service():
    return MovieRecommenderService.get_instance()
