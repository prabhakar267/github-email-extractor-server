import json

import requests

GITHUB_URL = "https://api.github.com/"


def __get_json_response(url):
    response = requests.get(url)
    return json.loads(response.text)


def __get_github_emails(user):
    try:
        users_profile_url = GITHUB_URL + "users/{0}".format(user)
        response = __get_json_response(users_profile_url)

        # some error encountered
        if 'message' in response:
            if response['message'] == 'Not Found':
                return u'You need to enter a valid GitHub Username'
            else:
                return response['message']

        user_name = response['name']

        # if user has a public email, add that to the set of emails
        if response['email']:
            return response['email']

        users_repository_url = GITHUB_URL + "users/{0}/repos?type=owner&sort=updated".format(user)
        response = __get_json_response(users_repository_url)

        for repo in response:
            if not repo['fork']:
                users_repository_name = repo['full_name']
                repos_commit_url = GITHUB_URL + "repos/{0}/commits".format(users_repository_name)
                commit_reponse = __get_json_response(repos_commit_url)

                possible_positions = ['committer', 'author']

                for commit in commit_reponse:
                    for i in possible_positions:
                        if commit['commit'][i]['name'] == user_name:
                            email_string = commit['commit'][i]['email']
                            if "noreply" not in email_string:
                                return email_string

    except requests.exceptions.ConnectionError:
        return u'Proper internet connection not found'
