from dotenv import load_dotenv
import requests
import time
from os import getenv
load_dotenv()

def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={getenv('TMDB_API_KEY')}"
    response = requests.get(url)
    if response.status_code == 429:
        time.sleep(1)
        return get_poster(movie_id)

    if response.status_code != 200:
        return None

    data = response.json()
    poster_path = data.get("poster_path")

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    return None