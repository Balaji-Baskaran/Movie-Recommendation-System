import json
import logging
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from pathlib import Path
from django.conf import settings
from .recommender import recommend
from .chart_heartbeat import make_heartbeat_chart
from .services import get_service

logger = logging.getLogger("movies")


def index(request):
    """Serve the built React single-page app."""
    dist_index = Path(settings.ROOT_DIR) / "frontend" / "dist" / "index.html"
    if dist_index.exists():
        with open(dist_index, "r", encoding="utf-8") as f:
            return HttpResponse(f.read(), content_type="text/html")
    return HttpResponse(
        "<h1>Movie Recommendation System Backend Running</h1><p>Run 'npm run build' in frontend/ to serve React directly here, or run 'npm run dev' on port 5173.</p>"
    )



@require_GET
def api_health(request):
    """Health check endpoint."""
    service = get_service()
    return JsonResponse({
        "status": "healthy",
        "service": "Movie Recommendation System (Django API)",
        "movies_loaded": len(service.df),
    })


@require_GET
def api_movies(request):
    """Return list of all movies for the search dropdown."""
    service = get_service()
    return HttpResponse(service.movie_options_json, content_type="application/json")


@require_GET
def api_filter_options(request):
    """Return genre, year, and industry options for the filter dropdowns."""
    service = get_service()
    return HttpResponse(service.filter_options_json, content_type="application/json")


@csrf_exempt
@require_POST
def api_search(request):
    """
    POST body: { "movie_idx": int, "n": int }
    Returns: selected movie info + chart JSON + top-N recommendations
    """
    try:
        body = json.loads(request.body.decode("utf-8") if request.body else "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    try:
        movie_idx = int(body.get("movie_idx", 0))
        n = int(body.get("n", 10))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    service = get_service()
    df = service.df
    emb_norm = service.emb_norm

    if movie_idx < 0 or movie_idx >= len(df):
        logger.warning(f"SEARCH │ Invalid movie_idx={movie_idx} requested")
        return JsonResponse({"error": "Invalid movie index"}, status=400)

    sm = df.iloc[movie_idx]
    movie_title = str(sm["title"])
    movie_year = int(sm["year"]) if pd.notna(sm.get("year")) else 0

    logger.info(
        f"SEARCH │ '{movie_title}' ({movie_year}) │ idx={movie_idx} │ top-{n} recommendations requested"
    )

    # Selected movie payload
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

    # Recommendations
    recs = recommend(movie_idx, df, emb_norm, n=n)

    top_titles = ", ".join(f"'{r['title']}'" for r in recs[:3])
    logger.info(f"RESULT │ '{movie_title}' │ Top matches: {top_titles} ...")

    # Heartbeat chart → JSON
    fig = make_heartbeat_chart(recs, sm["title"])
    chart_json = fig.to_json()

    return JsonResponse({
        "selected": selected,
        "recommendations": recs,
        "chart_json": chart_json,
    })


@csrf_exempt
@require_POST
def api_filter(request):
    """
    POST body: { "genres": [...], "years": [...], "industries": [...] }
    Returns: { "movies": [...] }
    """
    try:
        body = json.loads(request.body.decode("utf-8") if request.body else "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

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
        return JsonResponse({"movies": [], "error": "No movies found matching these criteria."})

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

    return JsonResponse({"movies": movies})
