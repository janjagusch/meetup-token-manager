"""
Helper methods for the tests.
"""

import gzip
import json
import os
import time

from dotenv import load_dotenv
import pytest
from redis import Redis

from meetup import TokenCache
from meetup.token import Token
from meetup.token_client import TokenClient


load_dotenv()


def scrub_access_token():
    """
    Removes the confidential properties from a token response.
    """

    def before_record_response(response):
        token = {
            "access_token": "ACCESS_TOKEN",
            "refresh_token": "REFRESH_TOKEN",
            "token_type": "bearer",
            "expires_in": 3600,
        }

        response["body"]["string"] = gzip.compress(json.dumps(token).encode())

        return response

    return before_record_response


@pytest.fixture(name="vcr", scope="module")
def vcr_(vcr):
    """
    vcr.
    """
    vcr.filter_post_data_parameters = [
        ("client_id", "CLIENT_ID"),
        ("client_secret", "CLIENT_SECRET"),
        ("redirect_uri", "REDIRECT_URI"),
        ("code", "CODE"),
    ]
    vcr.before_record_response = scrub_access_token()
    vcr.match_on = ["method", "scheme", "port", "path"]
    return vcr


@pytest.fixture(name="client_id")
def client_id_():
    """
    client_id.
    """
    return os.environ.get("CLIENT_ID", "CLIENT_ID")


@pytest.fixture(name="client_secret")
def client_secret_():
    """
    client_secret.
    """
    return os.environ.get("CLIENT_SECRET", "CLIENT_SECRET")


@pytest.fixture(name="redirect_uri")
def redirect_uri_():
    """
    redirect_uri.
    """
    return os.environ.get("REDIRECT_URI", "REDIRECT_URI")


@pytest.fixture(name="code")
def code_():
    """
    code.
    """
    return os.environ.get("CODE", "CODE")


@pytest.fixture(name="redis_client")
def redis_client_():
    """
    redis_client.
    """
    redis_url = os.environ.get(
        "REDIS_URL", "redis://@localhost:6379?db=0&decode_responses=True"
    )
    return Redis.from_url(redis_url)


@pytest.fixture(name="token_cache")
def token_cache_(client_id, client_secret, redirect_uri, redis_client):
    """
    token_cache.
    """
    return TokenCache(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        redis_client=redis_client,
    )


@pytest.fixture(name="token_client", scope="function")
def token_client_(client_id, client_secret, redirect_uri):
    """
    make_token_client.
    """
    return TokenClient(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
    )


@pytest.fixture(name="cache_key")
def cache_key_(client_id):
    """
    cache_key.
    """
    return f"oauth_token_cache__{client_id}"


@pytest.fixture(name="access_token")
def access_token_():
    """
    access_token.
    """
    return os.environ.get("ACCESS_TOKEN", "ACCESS_TOKEN")


@pytest.fixture(name="token_type")
def token_type_():
    """
    token_type.
    """
    return os.environ.get("TOKEN_TYPE", "bearer")


@pytest.fixture(name="refresh_token")
def refresh_token_():
    """
    refresh_token.
    """
    return os.environ.get("REFRESH_TOKEN", "REFRESH_TOKEN")


@pytest.fixture(name="expires_in")
def expires_in_():
    """
    expires_in.
    """
    return os.environ.get("EXPIRES_IN", 3600)


@pytest.fixture(name="expires_at")
def expires_at_(expires_in):
    """
    expires_at.
    """
    return int(time.time()) + expires_in


@pytest.fixture(name="token", scope="function")
def token_(access_token, token_type, refresh_token, expires_at):
    """
    token.
    """
    return Token(
        access_token=access_token,
        token_type=token_type,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )
