"""
Tests for the `meetup.token_cache` module.
"""

import time

import pytest

from meetup.exceptions import NoCachedTokenError
from meetup.token import Token


# pylint: disable=protected-access, pointless-statement


class TestTokenCache:
    """
    This class provided tests for the `meetup.token_cache.TokenCache` class
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
        TestTokenCache._setup(redis_client)
        yield
        TestTokenCache._teardown(redis_client)

    @staticmethod
    def test__cache_key(token_cache, client_id):
        assert token_cache._cache_key == f"oauth_token_cache__{client_id}"

    @staticmethod
    def test__cache_token(token_cache, token):
        token_cache._cache_token(token)
        assert token_cache.cached_token() == token

    @staticmethod
    def test_cached_token_empty(token_cache):
        assert token_cache.cached_token() is None

    @staticmethod
    @pytest.mark.vcr()
    def test_authorize(token_cache, code):
        token_cache.authorize(code)
        assert isinstance(token_cache.token, Token)

    @staticmethod
    def test_token_memory(token_cache, token):
        token_cache._token = token

        new_token = token_cache.token
        assert isinstance(new_token, Token)
        assert new_token == token
        assert token_cache._token == new_token

    @staticmethod
    def test_token_no_memory_cache(token_cache, token):
        token_cache._cache_token(token)

        new_token = token_cache.token
        assert isinstance(new_token, Token)
        assert new_token == token
        assert token_cache._token == new_token
        assert token_cache.cached_token() == new_token

    @staticmethod
    @pytest.mark.vcr()
    def test_token_no_memory_expired_cache(token_cache, token):
        token["expires_at"] = int(time.time())
        token_cache._cache_token(token)

        new_token = token_cache.token
        assert isinstance(new_token, Token)
        assert token_cache._token == new_token
        assert token_cache.cached_token() == new_token

    @staticmethod
    def test_token_no_memory_no_cache(token_cache):
        with pytest.raises(NoCachedTokenError):
            token_cache.token

    @staticmethod
    def test_token_expired_memory_cache(token_cache, token):
        token_cache._cache_token(token)
        token["expires_at"] = int(time.time())
        token_cache._token = token

        new_token = token_cache.token
        assert isinstance(new_token, Token)
        assert token_cache._token == new_token
        assert token_cache.cached_token() == new_token

    @staticmethod
    @pytest.mark.vcr()
    def test_token_expired_memory_expired_cache(token_cache, token):
        token["expires_at"] = int(time.time())
        token_cache._token = token
        token_cache._cache_token(token)

        new_token = token_cache.token
        assert isinstance(new_token, Token)
        assert token_cache._token == new_token
        assert token_cache.cached_token() == new_token

    @staticmethod
    def test_token_expired_memory_no_cache(token_cache, token):
        token["expires_at"] = int(time.time())
        token_cache._token = token

        with pytest.raises(NoCachedTokenError):
            token_cache.token
