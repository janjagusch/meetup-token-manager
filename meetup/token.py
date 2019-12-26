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
    def from_api(cls, *, access_token, token_type, refresh_token, expires_in):
        """
        Initializes a fresh token from the API.

        Args:
            access_token (str): The access token.
            expires_in (int): Total number of seconds until token will expire. This
                assumes that the token has been created now.
            token_type (str): The token type.
            refresh_token (str): The refresh token.

        Returns:
            Token: An instance of Token.
        """
        expires_at = int(time.time()) + expires_in

        return cls(
            access_token=access_token,
            expires_at=expires_at,
            token_type=token_type,
            refresh_token=refresh_token,
        )

    @classmethod
    def from_cache(cls, cached_token):
        """
        Initializes a cached token from Redis.

        Args:
            cached_token (dict): The cached token.

        Returns:
            Token: An instance of Token.
        """
        cached_token["expires_at"] = int(cached_token["expires_at"])
        return cls(**cached_token)

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
        return int(time.time()) > self.expires_at
