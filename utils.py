import logging
import os

import requests

GITHUB_BASE_API_URL = "https://api.github.com"

GITHUB_USER_API_URL = "{base_url}/users/{0}"
GITHUB_USER_REPO_API_URL = "{base_url}/users/{0}/repos?type=owner&sort=updated"
GITHUB_REPO_COMMITS_API_URL = "{base_url}/repos/{0}/commits"

possible_positions = ['committer', 'author']
master_username = os.environ.get("GITHUB_USERNAME")
master_password = os.environ.get("GITHUB_PASSWORD")


def get_api_response(url):
    try:
        use_credentials = True if os.environ.get('USE_CREDENTIALS', "0") == "1" else False
        if use_credentials:
            response = requests.get(url, auth=(master_username, master_password))
        else:
            response = requests.get(url)

        if response.status_code == 401:
            logging.error("Invalid Credentials. Disabling for future")
            os.environ['USE_CREDENTIALS'] = "0"
            return get_api_response(url)
        if response.ok:
            return response.json()
    except Exception as e:
        logging.exception(e)
        return None
    return None


def get_email(username):
    users_profile_url = GITHUB_USER_API_URL.format(username, base_url=GITHUB_BASE_API_URL)
    response = get_api_response(users_profile_url)

    if not response:
        return None

    # if user has a public email, add that to the set of emails
    if response['email']:
        logging.info("Public email found for user")
        return response['email']

    user_name = response['name']
    users_repository_url = GITHUB_USER_REPO_API_URL.format(username, base_url=GITHUB_BASE_API_URL)
    response = get_api_response(users_repository_url)

    if not response:
        logging.error("No public source repository for user")
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

    logging.error("No email found in {} source repositories".format(len(response)))
    return None
