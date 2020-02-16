# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python (meetup-token-cache)
#     language: python
#     name: meetup-token-cache
# ---

import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)

sys.path.append("..")

from redis import Redis
from dotenv import load_dotenv
import requests

from meetup import TokenCache

load_dotenv()

# +
VALID_SCOPES = [
    "ageless",
    "basic",
    "event_management",
    "group_edit",
    "group_content_edit",
    "group_join",
    "messaging",
    "profile_edit",
    "reporting",
    "rsvp",
]


def request_authorization_url(key, redirect_uri, scope=None):
    scope = set(scope or [])
    assert scope.issubset(VALID_SCOPES)
    scope = "+".join(scope)
    response_type = "code"

    return (
        "https://secure.meetup.com/oauth2/authorize"
        f"?client_id={key}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type={response_type}"
        f"&scope={scope}"
    )


# -

import yaml

with open(
    "../tests/cassettes/TestTokenClient.test_fresh_token_create.yaml"
) as file_pointer:
    casette = yaml.full_load(file_pointer)

b = casette["interactions"][0]["response"]["body"]["string"]

import gzip

gzip.decompress(b).decode("utf-8")

print(request_authorization_url(os.environ["CLIENT_ID"], os.environ["REDIRECT_URI"]))

code = "447cac48893fb8922c531c3333be02cc"

redis_client = Redis.from_url(
    os.environ.get("REDIS_URL", "redis://@localhost:6379?db=0&decode_responses=True")
)

redis_client.keys()

token_cache = TokenCache(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URI"],
    redis_client=redis_client,
)

token_cache.token(refresh=True, code=code)

redis_client.keys()

token_cache.token()
