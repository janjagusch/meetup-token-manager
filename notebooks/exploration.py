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

print(request_authorization_url(os.environ["CLIENT_ID"], os.environ["REDIRECT_URI"]))

code = "ca1915cb04e69295ee99c31548750bd8"

redis_client = Redis.from_url(os.environ["REDIS_URL"])

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
