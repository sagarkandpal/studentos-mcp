import sys
import os
import requests

sys.path.append(os.path.dirname(__file__))
from github_client import get_headers, BASE_URL


def _find_full_repo_name(repo_name: str):
    """
    Look through the user's actual repo list to find the exact
    owner/repo path — this avoids guessing the wrong owner.
    """
    response = requests.get(
        f"{BASE_URL}/user/repos",
        headers=get_headers(),
        params={"per_page": 100},
    )
    response.raise_for_status()
    repos = response.json()

    for repo in repos:
        if repo["name"].lower() == repo_name.lower():
            return repo["full_name"]  # e.g. "sagar/eazMeal"

    return None


def get_commits(repo_name: str):
    """
    Get the most recent commits for one of the user's repos.
    repo_name should just be the repo name (e.g. "studentos-mcp").
    """
    full_name = _find_full_repo_name(repo_name)
    if full_name is None:
        return f"No repo named '{repo_name}' found in your GitHub account."

    response = requests.get(
        f"{BASE_URL}/repos/{full_name}/commits",
        headers=get_headers(),
        params={"per_page": 5},
    )

    if response.status_code != 200:
        return f"GitHub API error {response.status_code}: {response.json().get('message', 'unknown error')}"

    commits = response.json()
    return [
        {
            "message": c["commit"]["message"],
            "date": c["commit"]["author"]["date"],
        }
        for c in commits
    ]