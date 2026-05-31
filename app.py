from fastapi import FastAPI
import requests
from scraper import parse_archive, find_movie_block, extract_streams

app = FastAPI()

ARCHIVE_URL = "One_Page_Archive.html"
with open(ARCHIVE_URL, "r", encoding="utf-8") as f:
    html = f.read()

print("ARCHIVE_URL has loaded")

@app.get("/manifest.json")
def manifest():
    return {
        "id": "com.nanas.onemovies",
        "version": "1.0.0",
        "name": "NaNas onemovies",
        "description": "Stremio addon for OneMovies archive",
        "resources": ["catalog", "meta", "stream"],
        "types": ["movie", "series"],
        "catalogs": [
            {
                "type": "movie",
                "id": "onemovies_movies",
                "name": "OneMovies Movies"
            }
        ]
    }


@app.get("/catalog/movie/onemovies_movies.json")
def catalog():
    items = parse_archive(html)

    return {"metas": items}


@app.get("/meta/movie/{imdb_id}.json")
def meta(imdb_id: str):
    movie = find_movie_block(html, imdb_id)

    if not movie:
        return {"meta": None}

    return {
        "meta": {
            "id": imdb_id,
            "type": "movie",
            "name": movie["title"],
            "description": f"IMDb Rating: {movie.get('rating', 'N/A')}",
            "imdbId": imdb_id
        }
    }


@app.get("/stream/movie/{imdb_id}.json")
def stream(imdb_id: str):
    streams = extract_streams(html, imdb_id)

    return {"streams": streams}
