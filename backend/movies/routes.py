import logging
import pandas as pd
from flask import Blueprint, jsonify, request, Response

from .recommender import recommend
from .chart_heartbeat import make_heartbeat_chart
from .services import get_service

logger = logging.getLogger("movies")

movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/health", methods=["GET"])
def api_health():
    """Health check endpoint."""
    service = get_service()
    return jsonify({
        "status": "healthy",
        "service": "Movie Recommendation System (Flask API)",
        "movies_loaded": len(service.df),
    })


@movies_bp.route("/movies", methods=["GET"])
def api_movies():
    """Return list of all movies for the search dropdown."""
    service = get_service()
    return Response(service.movie_options_json, mimetype="application/json")


@movies_bp.route("/filter-options", methods=["GET"])
def api_filter_options():
    """Return genre, year, and industry options for the filter dropdowns."""
    service = get_service()
    return Response(service.filter_options_json, mimetype="application/json")


@movies_bp.route("/search", methods=["POST"])
def api_search():
    """
    POST body: { "movie_idx": int, "n": int }
    Returns: selected movie info + chart JSON + top-N recommendations
    """
    body = request.get_json(silent=True)
    if body is None or not isinstance(body, dict):
        return jsonify({"error": "Invalid JSON format"}), 400

    try:
        movie_idx = int(body.get("movie_idx", 0))
        n = int(body.get("n", 10))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid parameters"}), 400

    service = get_service()
    df = service.df
    emb_norm = service.emb_norm

    if movie_idx < 0 or movie_idx >= len(df):
        logger.warning(f"SEARCH │ Invalid movie_idx={movie_idx} requested")
        return jsonify({"error": "Invalid movie index"}), 400

    sm = df.iloc[movie_idx]
    movie_title = str(sm["title"])
    movie_year = int(sm["year"]) if pd.notna(sm.get("year")) else 0

    logger.info(
        f"SEARCH │ '{movie_title}' ({movie_year}) │ idx={movie_idx} │ top-{n} recommendations requested"
    )

    selected = {
        "title": movie_title,
        "industry": str(sm["industry"]),
        "year": movie_year,
        "rating": float(sm["rating"]) if pd.notna(sm.get("rating")) else 0.0,
        "popularity": float(sm["popularity"]) if pd.notna(sm.get("popularity")) else 0.0,
        "overview": str(sm["overview"]) if pd.notna(sm.get("overview")) else "",
        "poster_path": str(sm["poster_path"]) if pd.notna(sm.get("poster_path")) else "",
        "genre_list": sm["genre_list"] if isinstance(sm.get("genre_list"), list) else [],
    }

    recs = recommend(movie_idx, df, emb_norm, n=n)

    top_titles = ", ".join(f"'{r['title']}'" for r in recs[:3])
    logger.info(f"RESULT │ '{movie_title}' │ Top matches: {top_titles} ...")

    fig = make_heartbeat_chart(recs, sm["title"])
    chart_json = fig.to_json()

    return jsonify({
        "selected": selected,
        "recommendations": recs,
        "chart_json": chart_json,
    })


@movies_bp.route("/filter", methods=["POST"])
def api_filter():
    """
    POST body: { "genres": [...], "years": [...], "industries": [...] }
    Returns: { "movies": [...] }
    """
    body = request.get_json(silent=True)
    if body is None or not isinstance(body, dict):
        return jsonify({"error": "Invalid JSON format"}), 400

    sel_genres = body.get("genres", [])
    sel_years = body.get("years", [])
    sel_inds = body.get("industries", [])

    logger.info(
        f"FILTER │ genres={sel_genres or '(any)'} │ years={sel_years or '(any)'} │ industries={sel_inds or '(any)'}"
    )

    service = get_service()
    filtered = service.df

    if sel_years:
        try:
            sel_years = [int(y) for y in sel_years]
            filtered = filtered[filtered["year"].isin(sel_years)]
        except Exception:
            pass

    if sel_inds:
        filtered = filtered[filtered["industry"].isin(sel_inds)]

    if sel_genres:
        sel_genres_set = set(g.lower() for g in sel_genres)
        mask = filtered["genre_set"].apply(lambda x: sel_genres_set.issubset(x))
        filtered = filtered[mask]

    if filtered.empty:
        logger.warning("FILTER │ No results found for applied filters")
        return jsonify({"movies": [], "error": "No movies found matching these criteria."})

    filtered = filtered.sort_values(
        by=["rating", "popularity"], ascending=[False, False]
    ).head(20)

    logger.info(f"FILTER │ {len(filtered)} movies returned")

    movies = []
    for rank, (_, row) in enumerate(filtered.iterrows(), 1):
        movies.append({
            "rank": rank,
            "score": 0.0,
            "title": str(row["title"]),
            "industry": str(row["industry"]),
            "year": int(row["year"]) if pd.notna(row.get("year")) else 0,
            "rating": float(row["rating"]) if pd.notna(row.get("rating")) else 0.0,
            "popularity": float(row["popularity"]) if pd.notna(row.get("popularity")) else 0.0,
            "overview": str(row["overview"]) if pd.notna(row.get("overview")) else "",
            "poster_path": str(row["poster_path"]) if pd.notna(row.get("poster_path")) else "",
            "genre_list": row["genre_list"] if isinstance(row.get("genre_list"), list) else [],
        })

    return jsonify({"movies": movies})
