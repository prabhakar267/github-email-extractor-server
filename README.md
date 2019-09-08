# [GitHub Email Extractor](https://github.com/prabhakar267/github-email-extractor) Server
[![Build Status](https://travis-ci.org/prabhakar267/github-email-extractor-server.svg?branch=master)](https://travis-ci.org/prabhakar267/github-email-extractor-server)
> Server code for the chrome extension to fetch the email ID of a user even if they haven't made it public on their GitHub profile. Uses [Redis](https://redis.io) for caching.

[![Chrome Store](https://raw.githubusercontent.com/prabhakar267/github-classifier/master/assets/images/chrome-store.png)](https://github.com/prabhakar267/github-email-extractor)

### Setup Instructions

+ Setup environment
```
pip install virtualenv
virtualenv venv --python=python3.6
source venv/bin/activate
```
+ Install Redis.
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
```
+ Run server
```
python app.py
```
Open localhost:5000

### Troubleshooting
+ Follow [this](https://redis.io/topics/quickstart) page for Redis related issues.