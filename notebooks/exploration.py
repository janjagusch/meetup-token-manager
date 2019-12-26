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
#     display_name: Python (meetup-token-manager)
#     language: python
#     name: meetup-token-manager
# ---

import os
import sys

sys.path.append("..")

from redis import Redis
from dotenv import load_dotenv
import requests

from meetup import TokenManager

load_dotenv()

MEETUP_API_KEY = os.environ.get("MEETUP_API_KEY")
MEETUP_API_SECRET = os.environ.get("MEETUP_API_SECRET")
MEETUP_API_REDIRECT_URI = os.environ.get("MEETUP_API_REDIRECT_URI")

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

redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True,)

token_manager = TokenManager(
    MEETUP_API_KEY, MEETUP_API_SECRET, MEETUP_API_REDIRECT_URI, redis_client
)

token_manager.cached_token()

token_manager.fresh_token()

token_manager.cached_token()
