# Tool: get_file_content.py
import sys
import os
import requests
import base64

sys.path.append(os.path.dirname(__file__))
from github_client import get_headers, get_username, BASE_URL


def get_file_content(repo_name: str, file_path: str):
    """
    Read the content of one specific file inside one of the user's repos.
    file_path should be relative to the repo root, e.g. "src/main.py".
    """
    username = get_username()

    response = requests.get(
        f"{BASE_URL}/repos/{username}/{repo_name}/contents/{file_path}",
        headers=get_headers(),
    )

    if response.status_code != 200:
        return f"GitHub API error {response.status_code}: {response.json().get('message', 'unknown error')}"

    data = response.json()

    if data.get("type") != "file":
        return f"'{file_path}' is not a file (it might be a folder)."

    content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    return content