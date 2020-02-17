"""
Tests for the `meetup.token_cache.utils` module.
"""

import pytest

from meetup.token_cache import utils


@pytest.fixture(name="scopes")
def scopes_():
    return {}


@pytest.fixture(name="invalid_scopes")
def invalid_scopes_():
    return {"admin"}


def test_make_authorization_url(client_id, redirect_uri, scopes):
    url = utils.make_authorization_url(client_id, redirect_uri, scopes)
    assert isinstance(url, str)


def test_make_authorization_url_invalid(client_id, redirect_uri, invalid_scopes):
    with pytest.raises(ValueError):
        utils.make_authorization_url(client_id, redirect_uri, invalid_scopes)
