"""
Tests for the `meetup.token_client` module.
"""

import pytest

from meetup.token_cache.token import Token


class TestTokenClient:
    """
    This class provided tests for the `meetup.token_client.TokenClient` class
    """

    @staticmethod
    @pytest.mark.vcr()
    def test_refresh_token(token_client, token):
        assert isinstance(token_client.refresh_token(token.refresh_token), Token)

    @staticmethod
    @pytest.mark.vcr()
    def test_create_token(token_client, code):
        assert isinstance(token_client.create_token(code), Token)
