"""
Movie Recommendation System – Flask + Uvicorn (ASGI)
Run with:  uvicorn app:asgi_app --reload --port 8000
"""

from flask import Flask, jsonify, render_template, request, Response, g
import json
import time
import logging
from asgiref.wsgi import WsgiToAsgi
import pandas as pd

from libs.data_utils import load_model, prepare_data
from module.recommender import recommend
from views.chart_heartbeat import make_heartbeat_chart
from views.icons import icon

# ─── Logger setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("cinematch")

# ─── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

# ─── Load model & data at startup ─────────────────────────────────────────────
logger.info("Loading recommendation model...")
_raw      = load_model("model/movie_recommendation_model.pkl")
df, emb_norm = prepare_data(_raw)
df["genre_set"] = df["genre_list"].apply(lambda x: set(g.lower() for g in x if g) if isinstance(x, list) else set())
logger.info("Model loaded  │  %d movies in dataset", len(df))

INDUSTRIES = sorted(df["industry"].dropna().unique().tolist())

# Pre-build genre + year lists for filter options
def _get_filter_options():
    all_genres = set()
    for g_list in df["genre_list"].dropna():
        if isinstance(g_list, list):
            for g in g_list:
                if g:
                    all_genres.add(g.strip().title())
    all_years = sorted(
        [int(y) for y in df["year"].dropna().unique() if y > 0],
        reverse=True,
    )
    return sorted(list(all_genres)), all_years

GENRES, YEARS = _get_filter_options()

# Pre-build movie options list (idx → label) once
def _build_movie_options():
    opts = []
    for idx, row in df.iterrows():
        year_val = int(row["year"]) if pd.notna(row.get("year")) else 0
        label = f"{row['title']}  ({year_val}  ·  {row['industry']})"
        opts.append({"idx": int(idx), "label": label})
    return opts

MOVIE_OPTIONS = _build_movie_options()
MOVIE_OPTIONS_JSON = json.dumps(MOVIE_OPTIONS)
FILTER_OPTIONS_JSON = json.dumps({
    "genres":     GENRES,
    "years":      YEARS,
    "industries": INDUSTRIES,
})


# ─── Request logging hooks ───────────────────────────────────────────────────
@app.before_request
def _before():
    g.start_time = time.perf_counter()

@app.after_request
def _after(response):
    elapsed_ms = (time.perf_counter() - g.start_time) * 1000
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    status = response.status_code
    # Colour-code by status
    if status < 300:
        lvl = logging.INFO
    elif status < 400:
        lvl = logging.INFO
    else:
        lvl = logging.WARNING
    logger.log(
        lvl,
        "%s  %s  %s  %dms  [%s]",
        request.method,
        request.path,
        status,
        int(elapsed_ms),
        ip,
    )
    return response

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def index():
    logger.info("Page loaded → index.html")
    return render_template("index.html")


@app.get("/api/movies")
def api_movies():
    """Return list of all movies for the search dropdown."""
    return Response(MOVIE_OPTIONS_JSON, mimetype="application/json")


@app.get("/api/filter-options")
def api_filter_options():
    """Return genre, year, and industry options for the filter dropdowns."""
    return Response(FILTER_OPTIONS_JSON, mimetype="application/json")


@app.post("/api/search")
def api_search():
    """
    POST body: { "movie_idx": int, "n": int }
    Returns: selected movie info + chart JSON + top-N recommendations
    """
    body      = request.get_json(force=True)
    movie_idx = int(body.get("movie_idx", 0))
    n         = int(body.get("n", 10))

    if movie_idx < 0 or movie_idx >= len(df):
        logger.warning("SEARCH  │  Invalid movie_idx=%d requested", movie_idx)
        return jsonify({"error": "Invalid movie index"}), 400

    sm = df.iloc[movie_idx]
    movie_title = str(sm["title"])
    movie_year  = int(sm["year"]) if pd.notna(sm.get("year")) else 0

    logger.info(
        "SEARCH  │  '%s' (%s)  │  idx=%d  │  top-%d recommendations requested",
        movie_title, movie_year, movie_idx, n,
    )

    # Selected movie payload
    selected = {
        "title":       movie_title,
        "industry":    str(sm["industry"]),
        "year":        movie_year,
        "rating":      float(sm["rating"]) if pd.notna(sm.get("rating"))   else 0.0,
        "popularity":  float(sm["popularity"]) if pd.notna(sm.get("popularity")) else 0.0,
        "overview":    str(sm["overview"]) if pd.notna(sm.get("overview")) else "",
        "poster_path": str(sm["poster_path"]) if pd.notna(sm.get("poster_path")) else "",
        "genre_list":  sm["genre_list"] if isinstance(sm.get("genre_list"), list) else [],
    }

    # Recommendations
    recs = recommend(movie_idx, df, emb_norm, n=n)

    top_titles = ", ".join(f"'{r['title']}'" for r in recs[:3])
    logger.info(
        "RESULT  │  '%s'  │  Top matches: %s ...",
        movie_title, top_titles,
    )

    # Heartbeat chart → JSON
    fig = make_heartbeat_chart(recs, sm["title"])
    chart_json = fig.to_json()

    return jsonify({
        "selected":        selected,
        "recommendations": recs,
        "chart_json":      chart_json,
    })


@app.post("/api/filter")
def api_filter():
    """
    POST body: { "genres": [...], "years": [...], "industries": [...] }
    Returns: { "movies": [...] }
    """
    body       = request.get_json(force=True)
    sel_genres = body.get("genres",     [])
    sel_years  = body.get("years",      [])
    sel_inds   = body.get("industries", [])

    logger.info(
        "FILTER  │  genres=%s  │  years=%s  │  industries=%s",
        sel_genres or "(any)",
        sel_years  or "(any)",
        sel_inds   or "(any)",
    )

    filtered = df

    if sel_years:
        filtered = filtered[filtered["year"].isin(sel_years)]
    if sel_inds:
        filtered = filtered[filtered["industry"].isin(sel_inds)]
    if sel_genres:
        sel_genres_set = set(g.lower() for g in sel_genres)
        mask = filtered["genre_set"].apply(lambda x: sel_genres_set.issubset(x))
        filtered = filtered[mask]

    if filtered.empty:
        logger.warning("FILTER  │  No results found for applied filters")
        return jsonify({"movies": [], "error": "No movies found matching these criteria."})

    filtered = filtered.sort_values(
        by=["rating", "popularity"], ascending=[False, False]
    ).head(20)

    logger.info("FILTER  │  %d movies returned", len(filtered))

    movies = []
    for rank, (_, row) in enumerate(filtered.iterrows(), 1):
        movies.append({
            "rank":        rank,
            "score":       0.0,
            "title":       str(row["title"]),
            "industry":    str(row["industry"]),
            "year":        int(row["year"])   if pd.notna(row.get("year"))        else 0,
            "rating":      float(row["rating"]) if pd.notna(row.get("rating"))    else 0.0,
            "popularity":  float(row["popularity"]) if pd.notna(row.get("popularity")) else 0.0,
            "overview":    str(row["overview"]) if pd.notna(row.get("overview"))  else "",
            "poster_path": str(row["poster_path"]) if pd.notna(row.get("poster_path")) else "",
            "genre_list":  row["genre_list"] if isinstance(row.get("genre_list"), list) else [],
        })

    return jsonify({"movies": movies})


# ─── ASGI adapter for Uvicorn ──────────────────────────────────────────────────
asgi_app = WsgiToAsgi(app)

# ─── Dev fallback (python app.py) ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:asgi_app", host="127.0.0.1", port=8000, reload=True)