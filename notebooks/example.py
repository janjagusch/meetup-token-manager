# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python (meetup-token-cache)
#     language: python
#     name: meetup-token-cache
# ---

import os
import sys

sys.path.append("..")

from redis import Redis
from dotenv import load_dotenv

from meetup.token_cache import TokenCache
from meetup.token_cache.utils import make_authorization_url

load_dotenv()

redis_client = Redis.from_url(
    os.environ.get("REDIS_URL", "redis://@localhost:6379?db=0&decode_responses=True")
)

make_authorization_url(os.environ["CLIENT_ID"], os.environ["REDIRECT_URI"])

token_cache = TokenCache(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URI"],
    redis_client=redis_client,
)

token_cache.authorize(os.environ["CODE"])

token_cache.token
