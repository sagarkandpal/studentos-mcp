# Tool: search_repos.py
import sys
import os
import requests

sys.path.append(os.path.dirname(__file__))
from github_client import get_headers, BASE_URL


def search_repos(query: str):
    """
    Search ALL of GitHub (not just the user's own repos) for repositories
    matching a query — useful for finding example projects, inspiration, etc.
    """
    response = requests.get(
        f"{BASE_URL}/search/repositories",
        headers=get_headers(),
        params={"q": query, "sort": "stars", "order": "desc", "per_page": 10},
    )

    if response.status_code != 200:
        return f"GitHub API error {response.status_code}: {response.json().get('message', 'unknown error')}"

    repos = response.json()["items"]

    return [
        {
            "name": repo["full_name"],
            "description": repo["description"] or "No description",
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
        }
        for repo in repos
    ]