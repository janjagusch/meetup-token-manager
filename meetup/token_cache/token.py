"""
This module contains the Token class.
"""

import time


class Token(dict):

    """
    An access token for the Meetup API.

    Args:
        access_token (str): The actual access token.
        token_type (str): The token type.
        refresh_token (str): The refresh token.
        expires_at (int): The UNIX timestamp when the token expires.
    """

    def __init__(self, *, access_token, token_type, refresh_token, expires_at):
        super().__init__(self)
        self["access_token"] = access_token
        self["token_type"] = token_type
        self["refresh_token"] = refresh_token
        self["expires_at"] = expires_at

    @classmethod
    def from_api(cls, token_from_api):
        """
        Initializes a fresh token from the API.

        Args:
            token_from_api (dict): The token from the API.

        Returns:
            Token: An instance of Token.
        """
        token_from_api["expires_at"] = int(time.time()) + int(
            token_from_api["expires_in"]
        )
        token_from_api.pop("expires_in")

        return cls(**token_from_api)

    @classmethod
    def from_cache(cls, token_from_cache):
        """
        Initializes a cached token from Redis.

        Args:
            token_from_cache (dict): The cached token.

        Returns:
            Token: An instance of Token.
        """
        token_from_cache["expires_at"] = int(token_from_cache["expires_at"])
        return cls(**token_from_cache)

    @property
    def access_token(self):
        """
        The access token.
        """
        return self["access_token"]

    @property
    def token_type(self):
        """
        The token type.
        """
        return self["token_type"]

    @property
    def refresh_token(self):
        """
        The refresh token.
        """
        return self["refresh_token"]

    @property
    def expires_at(self):
        """
        The expires at timestamp.
        """
        return self["expires_at"]

    @property
    def expires_in(self):
        """
        The number of seconds until the token expires.
        """
        return int(self.expires_at - time.time())

    @property
    def expired(self):
        """
        Checks whether or not the access token has expired.
        """
        return self.expires_in <= 0
