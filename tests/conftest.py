"""
Helper methods for the tests.
"""

import os
import time

from dotenv import load_dotenv
import pytest
from redis import Redis

from meetup import TokenCache
from meetup.token import Token
from meetup.token_client import TokenClient


load_dotenv()


@pytest.fixture(scope="module")
def vcr_config():
    """
    vcr_config.
    """
    return {
        "filter_headers": [("Authorization", "XXX")],
    }


@pytest.fixture(name="vcr", scope="module")
def vcr_(vcr):
    """
    vcr.
    """
    vcr.filter_post_data_parameters = [
        ("refresh_token", "secret"),
    ]
    vcr.match_on = ["method", "scheme", "port", "path", "body", "query"]
    return vcr


@pytest.fixture(name="client_id")
def client_id_():
    """
    client_id.
    """
    return os.environ["CLIENT_ID"]


@pytest.fixture(name="client_secret")
def client_secret_():
    """
    client_secret.
    """
    return os.environ["CLIENT_SECRET"]


@pytest.fixture(name="redirect_uri")
def redirect_uri_():
    """
    redirect_uri.
    """
    return os.environ["REDIRECT_URI"]


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


@pytest.fixture
def make_token_client(client_id, client_secret, redirect_uri, redis_client):
    TOKEN_CLIENT_DEFAULTS = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "redis_client": redis_client,
    }

    def _make_token_client(**kwargs):
        return TokenClient(**{**TOKEN_CLIENT_DEFAULTS, **kwargs})

    return _make_token_client


@pytest.fixture(name="cache_key")
def cache_key_(client_id):
    """
    cache_key.
    """
    return f"oauth_token_cache__{client_id}"


@pytest.fixture(name="access_token")
def access_token_():
    return "access token"


@pytest.fixture(name="token_type")
def token_type_():
    return "bearer"


@pytest.fixture(name="refresh_token")
def refresh_token_():
    return "refresh token"


@pytest.fixture(name="expires_in")
def expires_in_():
    return 3600


@pytest.fixture(name="expires_at")
def expires_at_(expires_in):
    return int(time.time()) + expires_in


@pytest.fixture(name="token")
def token_(access_token, token_type, refresh_token, expires_at):
    return Token(
        access_token=access_token,
        token_type=token_type,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )


@pytest.fixture
def make_token(access_token, token_type, refresh_token, expires_at):
    TOKEN_DEFAULTS = {
        "access_token": access_token,
        "token_type": token_type,
        "refresh_token": refresh_token,
        "expires_at": expires_at,
    }

    def _make_token(**kwargs):
        return Token(**{**TOKEN_DEFAULTS, **kwargs})

    return _make_token
