import os
import pytest
import requests

from meetup.token import Token


class TestTokenClient:
    def _setup(redis_client):
        assert not redis_client.keys()

    def _teardown(redis_client):
        redis_client.flushall()

    @staticmethod
    def setup_teardown(redis_client):
        TestTokenClient._setup()
        yield
        TestTokenClient._teardown()

    @staticmethod
    def test_cache_token(make_token_client, token):
        token_client = make_token_client()
        token_client.cache_token(token)
        assert token_client.cached_token() == token


def test_cache_key(make_token_client):
    token_client = make_token_client(client_id="XXX")

    assert token_client.cache_key == "oauth_token_cache__XXX"
