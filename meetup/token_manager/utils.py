"""
Helper functions for the `.token_cache` package.
"""

import datetime
import functools
import logging

import requests

from meetup.token_manager.token import Token


_LOGGER = logging.getLogger(__name__)


def _add_expires_at(func):
    """
    Adds 'expires_at' property to token dictionary.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        obj = func(*args, **kwargs)
        obj["expires_at"] = int(datetime.datetime.now().timestamp()) + obj["expires_in"]
        return obj

    return wrapper


def _convert_to_token(func):
    """
    Converts token dictionary to Token class.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return Token.from_dict(func(*args, **kwargs))

    return wrapper


@_convert_to_token
@_add_expires_at
def refresh_token(client_id, client_secret, refresh_token_):
    """
    Requests to refresh a token and returns a new token.
    """
    _LOGGER.info("Refreshing token.")
    res = requests.post(
        "https://secure.meetup.com/oauth2/access",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token_,
        },
    )
    res.raise_for_status()
    return res.json()


def _make_authorization_url(client_id, redirect_uri, scope=None):
    """
    Generates an authorization url for the Meetup API.

    Args:
        client_id (str): The key of your consumer.
        redirect_uri (str): The redirect uri of your consumer.
        scope (list): A list of scopes you want to give to the consumer. More
            information about scopes here: https://www.meetup.com/meetup_api/auth/.

    Returns:
        str: The url you need to visit to authorize the consumer.

    Raises:
        ValueError: When providing invalid scopes.
    """
    scope = set(scope or [])
    valid_scopes = [
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
    if not scope.issubset(valid_scopes):
        raise ValueError(f"Scope '{scope}' is not a subset of '{valid_scopes}'")

    scope_str = "+".join(scope)
    response_type = "code"

    return (
        "https://secure.meetup.com/oauth2/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type={response_type}"
        f"&scope={scope_str}"
    )


@_convert_to_token
@_add_expires_at
def _request_token(client_id, client_secret, redirect_uri, code):
    """
    Requests a new token.
    """
    _LOGGER.info("Requesting token.")
    res = requests.post(
        "https://secure.meetup.com/oauth2/access",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    res.raise_for_status()
    return res.json()


def request_token(client_id, client_secret, redirect_uri, scope=None):
    """
    Generates authorization url and waits for user to provide authorization code,
    then requests new API token.
    """
    url = _make_authorization_url(client_id, redirect_uri, scope)
    code = input(
        f"Please navigate to '{url}' and authorize the application.\n"
        "Next, paste the 'code' parameter from the redirect url here:\n"
    )
    return _request_token(client_id, client_secret, redirect_uri, code)
