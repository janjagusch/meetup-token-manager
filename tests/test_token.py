"""
Tests for the meetup.token_cache.token.Token class.
"""

import time

import pytest

from meetup.token_cache.token import Token


@pytest.fixture(name="token_from_cache")
def token_from_cache_(access_token, token_type, refresh_token, expires_at):
    """
    Token from Redis cache.
    """
    return {
        "access_token": access_token,
        "token_type": token_type,
        "refresh_token": refresh_token,
        "expires_at": str(expires_at),
    }


@pytest.fixture(name="token_from_api")
def token_from_api_(access_token, token_type, refresh_token, expires_in):
    """
    Token from api.
    """
    return {
        "access_token": access_token,
        "token_type": token_type,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
    }


def _validate_token(
    token, access_token, token_type, refresh_token, expires_at, expires_in, expired
):
    """
    Validates a token.
    """
    assert isinstance(token, Token)
    assert token.access_token == access_token
    assert token.token_type == token_type
    assert token.refresh_token == refresh_token
    assert token.expires_at == expires_at
    assert token.expires_in == expires_in
    assert token.expired == expired


def test_from_cache(
    token_from_cache, access_token, token_type, refresh_token, expires_at, expires_in
):

    token = Token.from_cache(token_from_cache)
    _validate_token(
        token,
        access_token,
        token_type,
        refresh_token,
        expires_at,
        expires_in - 1,
        False,
    )


def test_from_api(
    token_from_api, access_token, token_type, refresh_token, expires_at, expires_in
):

    token = Token.from_api(token_from_api)
    _validate_token(
        token,
        access_token,
        token_type,
        refresh_token,
        expires_at,
        expires_in - 1,
        False,
    )


def test_expired_token(access_token, token_type, refresh_token):

    expires_at = int(time.time())

    token = Token(
        access_token=access_token,
        token_type=token_type,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )
    _validate_token(token, access_token, token_type, refresh_token, expires_at, 0, True)
