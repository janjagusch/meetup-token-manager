"""
This module contains the TokenClient class.
"""

import logging

import requests

from .token import Token


class TokenClient:

    """
    TokenClient

    Retrieve OAuth 2.0 tokens from the token endpoint.

    Args:
        client_id (str): The client id.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect uri.

    Attributes:
        client_id (str): The client id.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect uri.
        _URL (str): The URL to the Meetup API.
    """

    _URL = "https://secure.meetup.com/oauth2/access"

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def _data(self, grant_type):
        """
        Data for token request against API.

        Args:
            grant_type (str): 'refresh_token' or 'create'

        Returns:
            dict: Data for token request.
        """
        return dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            grant_type=grant_type,
        )

    def _request_token(self, data):
        """
        Requests a token from the API and stores the result in `self.token`.

        Args:
            data (dict): Request post data for the API.

        Returns:
            Token: An instance of class `Token`.

        """
        response = requests.post(url=self._URL, data=data)
        response.raise_for_status()

        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response url: {response.url}")
        logging.debug(f"Response body: {response.json()}")
        response = response.json()

        return Token.from_api(response)

    def refresh_token(self, refresh_token):
        """
        Refreshes the token.

        Returns:
            Token: An instance of class `Token`.

        Raises:
            NoCachedTokenError: When there is no cached token.
        """
        logging.debug("Refreshing token.")

        grant_type = "refresh_token"
        data = self._data(grant_type)
        data["refresh_token"] = refresh_token

        return self._request_token(data)

    def create_token(self, code):
        """
        Creates a new token.

        Args:
            code (str): The authorization code.

        Returns:
            Token: An instance of class `Token`.
        """
        logging.debug("Creating token.")

        grant_type = "authorization_code"
        data = self._data(grant_type)
        data["code"] = code

        return self._request_token(data)
