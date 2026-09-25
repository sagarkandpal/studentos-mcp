import sys
import os

sys.path.append(os.path.dirname(__file__))
from github_client import get_headers, get_username, BASE_URL
import requests


def search_code(query: str, repo_name: str = None):
    """
    Search code across the user's GitHub. If repo_name is given,
    search is limited to just that repo.
    """
    search_query = query
    if repo_name:
        username = get_username()
        search_query += f" repo:{username}/{repo_name}"

    response = requests.get(
        f"{BASE_URL}/search/code",
        headers=get_headers(),
        params={"q": search_query},
    )
    response.raise_for_status()
    results = response.json()["items"]

    return [
        {"file": item["name"], "path": item["path"], "repo": item["repository"]["name"]}
        for item in results
    ]