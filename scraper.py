from bs4 import BeautifulSoup


def parse_archive(html: str):
    """
    Extract catalog items from OneMovies archive page
    """

    soup = BeautifulSoup(html, "html.parser")

    items = []

    for h3 in soup.find_all("h3"):

        title = h3.text.replace("start_year", "").strip()

        imdb_p = h3.find_next("p")

        if not imdb_p:
            continue

        if "IMDb Code:" not in imdb_p.text:
            continue

        imdb_id = imdb_p.text.replace("IMDb Code:", "").strip()

        items.append({
            "id": imdb_id,
            "type": "movie",
            "name": title
        })

    return items


def find_movie_block(html: str, imdb_id: str):
    """
    Find metadata for a single movie
    """

    soup = BeautifulSoup(html, "html.parser")

    for h3 in soup.find_all("h3"):

        imdb_p = h3.find_next("p")

        if imdb_p and imdb_id in imdb_p.text:

            title = h3.text.replace("start_year", "").strip()

            rating = None

            for p in h3.find_all_next("p", limit=10):

                if "IMDb Rates:" in p.text:
                    rating = p.text.replace("IMDb Rates:", "").strip()

            return {
                "title": title,
                "rating": rating
            }

    return None


def extract_streams(html: str, imdb_id: str):
    """
    Extract all video streams for a movie
    """

    soup = BeautifulSoup(html, "html.parser")

    streams = []

    for h3 in soup.find_all("h3"):

        imdb_p = h3.find_next("p")

        if imdb_p and imdb_id in imdb_p.text:

            links = h3.find_all_next("a", limit=50)

            for a in links:

                url = a.get("href")
                label = a.text.strip()

                if url and (".mkv" in url or "http" in url):

                    streams.append({
                        "title": label,
                        "url": url
                    })

            break

    return streams