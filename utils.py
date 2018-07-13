import json

import requests

GITHUB_BASE_API_URL = "https://api.github.com"

GITHUB_USER_API_URL = "{base_url}/users/{0}"
GITHUB_USER_REPO_API_URL = "{base_url}/users/{0}/repos?type=owner&sort=updated"
GITHUB_REPO_COMMITS_API_URL = "{base_url}/repos/{0}/commits"

possible_positions = ['committer', 'author']


def get_api_response(url):
    try:
        response = requests.get(url)
        if response.ok:
            return response.json()
    except Exception:
        return None
    return None


def get_email(username):
    users_profile_url = GITHUB_USER_API_URL.format(username, base_url=GITHUB_BASE_API_URL)
    response = get_api_response(users_profile_url)

    if not response:
        return None

    # if user has a public email, add that to the set of emails
    if response['email']:
        return response['email']

    user_name = response['name']
    users_repository_url = GITHUB_USER_REPO_API_URL.format(username, base_url=GITHUB_BASE_API_URL)
    response = get_api_response(users_repository_url)

    if not response:
        # No public source repository
        return None

    for repo in response:
        if not repo['fork']:
            users_repository_name = repo['full_name']
            repos_commit_url = GITHUB_REPO_COMMITS_API_URL.format(users_repository_name, base_url=GITHUB_BASE_API_URL)
            commit_response = get_api_response(repos_commit_url)

            if not commit_response:
                continue

            for commit in commit_response:
                for position in possible_positions:
                    if commit['commit'][position]['name'] == user_name:
                        email_string = commit['commit'][position]['email']
                        if "noreply" not in email_string:
                            return email_string
