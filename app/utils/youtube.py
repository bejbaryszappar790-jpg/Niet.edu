import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def parsing_youtube_url(url: str):
    pattern = r"[a-zA-Z0-9_-]{11}"

    result = re.search(pattern, url)

    if result:
        return result.group()
    else:
        return None


def get_youtube_metadata(url: str):
    result_of_parsing = parsing_youtube_url(url)

    if not result_of_parsing:
        return {"error": "Invalid URL"}

    API_KEY = os.getenv("GOOGLE_CONSOLE_API_KEY")

    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={result_of_parsing}&key={API_KEY}"
    response = requests.get(api_url)
    data = response.json()
    if not data.get("items"):
        return {"error": "Video not found in YouTube"}
    return data
