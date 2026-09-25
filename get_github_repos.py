import sys
import os

sys.path.append(os.path.dirname(__file__))
from github_client import get_headers, BASE_URL
import requests


def get_github_repos():
    """
    List the authenticated user's GitHub repositories (name + description).
    """
    response = requests.get(
        f"{BASE_URL}/user/repos",
        headers=get_headers(),
        params={"sort": "updated", "per_page": 10},  # only the 10 most recently updated
    )
    response.raise_for_status()
    repos = response.json()

    return [
        {"name": repo["name"], "description": repo["description"] or "No description"}
        for repo in repos
    ]