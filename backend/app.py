import logging
import os
import sys
from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from movies.routes import movies_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("app")

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
DIST_DIR = ROOT_DIR / "frontend" / "dist"


def create_app(test_config=None):
    """Application factory for the Flask backend."""
    app = Flask(
        __name__,
        static_folder=str(DIST_DIR / "assets") if (DIST_DIR / "assets").exists() else None,
        static_url_path="/assets",
    )

    # Configure CORS for frontend access
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    if test_config:
        app.config.update(test_config)

    # Register API blueprint under /api
    app.register_blueprint(movies_bp, url_prefix="/api")

    # Serve built React Single Page Application and its static assets
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        # Unmatched API routes return 404 JSON
        if path.startswith("api/") or path == "api":
            return jsonify({"error": "API endpoint not found"}), 404

        # Serve static assets from frontend/dist if they exist
        if path and DIST_DIR.exists():
            candidate = DIST_DIR / path
            if candidate.is_file():
                return send_from_directory(str(DIST_DIR), path)

        # Serve the single page app index.html
        index_file = DIST_DIR / "index.html"
        if index_file.exists():
            return send_from_directory(str(DIST_DIR), "index.html")

        return (
            "<h1>Movie Recommendation System Backend Running (Flask)</h1>"
            "<p>Run <code>npm run build</code> in <code>frontend/</code> to serve React directly here, "
            "or run <code>npm run dev</code> on port 5173 for development.</p>"
        )

    return app


app = create_app()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Movie Recommendation System Flask Server")
    parser.add_argument(
        "--host",
        type=str,
        default=os.environ.get("HOST", "127.0.0.1"),
        help="Host address to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", 5000)),
        help="Port number to listen on (default: 5000)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable Flask debug mode",
    )

    args = parser.parse_args()
    logger.info(f"Starting Flask server on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)
