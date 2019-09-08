import os

import redis
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from utils import get_email

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DEFAULT_EXPIRATION = 5184000  # 60 days


def _get_key(username):
    default_key_prefix = "githubExtractor"
    return "{}-{}".format(default_key_prefix, username.lower())


@app.route("/<string:github_username>", methods=['GET'])
@cross_origin()
def main(github_username):
    # check if the email was found earlier or not
    redis_key = _get_key(github_username)
    response = r.get(redis_key)
    if not response:
        response = get_email(github_username)
        if response:
            r.set(redis_key, response, ex=DEFAULT_EXPIRATION)
    if response:
        return "{0}".format(response), 200
    else:
        return "Invalid Request", 400


@app.route("/explore", methods=["GET"])
@cross_origin()
def get_all():
    all_emails = {}
    for item in r.scan_iter(_get_key("*")):
        all_emails[item] = r[item]
    return jsonify(all_emails)


@app.route("/", methods=["GET"])
@cross_origin()
def home_route():
    response = {
        "message": "Email missing. Usage <url>/<github_username>",
        "repository_url": "https://github.com/prabhakar267/github-email-extractor"
    }
    return jsonify(response), 404


if __name__ == "__main__":
    redis_url = os.getenv('REDISCLOUD_URL')
    if redis_url:
        r = redis.Redis.from_url(redis_url, decode_responses=True)
    else:
        r = redis.Redis(decode_responses=True)

    is_debug = os.getenv("IS_DEBUG", True)
    app.run(debug=is_debug, host="0.0.0.0", threaded=True)
