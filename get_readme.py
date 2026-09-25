# Tool: get_readme.py
import sys
import os
import requests
import base64

sys.path.append(os.path.dirname(__file__))
from github_client import get_headers, get_username, BASE_URL


def get_readme(repo_name: str):
    """
    Fetch and decode the README file content for one of the user's repos.
    """
    username = get_username()

    response = requests.get(
        f"{BASE_URL}/repos/{username}/{repo_name}/readme",
        headers=get_headers(),
    )

    if response.status_code != 200:
        return f"GitHub API error {response.status_code}: {response.json().get('message', 'unknown error')}"

    data = response.json()

    # GitHub returns file content as base64-encoded text — need to decode it
    content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")

    return content