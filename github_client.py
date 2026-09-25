import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"


def get_headers():
    """Standard headers needed for every GitHub API call."""
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def get_username():
    """Find out which GitHub account this token belongs to."""
    response = requests.get(f"{BASE_URL}/user", headers=get_headers())
    response.raise_for_status()  # raises an error if the request failed
    return response.json()["login"]