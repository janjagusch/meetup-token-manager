"""
Tests for the `meetup.token_client` module.
"""

import pytest

from meetup.token import Token


class TestTokenClient:
    """
    This class provided tests for the `meetup.token_client.TokenClient` class
    """

    @staticmethod
    def _setup(redis_client):
        """
        Setup before running a test.
        """
        assert not redis_client.keys()

    @staticmethod
    def _teardown(redis_client):
        """
        Teardowm after running a test.
        """
        redis_client.flushall()

    @staticmethod
    @pytest.fixture(autouse=True, scope="function")
    def setup_teardown(redis_client):
        """
        Setup and teardown before and after every test function call.
        """
        TestTokenClient._setup(redis_client)
        yield
        TestTokenClient._teardown(redis_client)

    @staticmethod
    def test_cache_token(token_client, token):
        token_client.cache_token(token)
        assert token_client.cached_token() == token

    @staticmethod
    @pytest.mark.vcr()
    def test_fresh_token_create(token_client, code):
        token_client.fresh_token(mode="create", code=code)
        assert isinstance(token_client.cached_token(), Token)

    @staticmethod
    @pytest.mark.vcr()
    def test_fresh_token_refresh(token_client, token):
        token_client.cache_token(token)
        token_client.fresh_token(mode="refresh")
        assert isinstance(token_client.cached_token(), Token)


def test_cache_key(token_client, client_id):
    assert token_client.cache_key == f"oauth_token_cache__{client_id}"
