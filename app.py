import json
import os

from flask import Flask, abort
from flask_cors import CORS, cross_origin
from utils import __get_github_emails

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

EMAIL_FILE = "email_file.json"


@app.route("/<string:github_username>", methods=['GET'])
@cross_origin()
def main(github_username):
    if not os.path.exists(EMAIL_FILE):
        with open(EMAIL_FILE, 'w+') as f:
            json.dump({}, f)
    with open(EMAIL_FILE, 'r+') as f:
        email_dict = json.load(f)

    # check if the email was found earlier or not
    if email_dict.get(github_username):
        return email_dict[github_username]
    response = __get_github_emails(github_username)
    if response:
        # add email to be used in future
        email_dict[github_username] = response
        with open(EMAIL_FILE, 'w+') as f:
            json.dump(email_dict, f)

        return "{0}".format(response)
    else:
        abort(404)


@app.route("/get-all", methods=["GET"])
@cross_origin()
def get_all():
    email_dict = {}
    if not os.path.exists(EMAIL_FILE):
        with open(EMAIL_FILE, 'w+') as f:
            json.dump(email_dict, f)

    with open(EMAIL_FILE, 'r+') as f:
        email_dict = json.load(f)
    return json.dumps(email_dict)


@app.errorhandler(404)
def page_not_found(error):
    return "Check https://github.com/prabhakar267/github-email-extractor for more details"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)
