"""
This module contains the token class.
"""

import datetime


class Token:
    """
    OAuth 2 token for Meetup API.
    """

    def __init__(self, access_token, refresh_token, token_type, expires_in, expires_at):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._token_type = token_type
        self._expires_in = expires_in
        self._expires_at = expires_at

    @property
    def access_token(self):
        """
        access_token
        """
        return self._access_token

    @property
    def refresh_token(self):
        """
        refresh_token
        """
        return self._refresh_token

    @property
    def token_type(self):
        """
        token_type
        """
        return self._token_type

    @property
    def expires_in(self):
        """
        expires_in
        """
        return self._expires_in

    @property
    def expires_at(self):
        """
        expires_at
        """
        return self._expires_at

    @property
    def expired(self):
        """
        expired
        """
        return datetime.datetime.now().timestamp() > self.expires_at

    def to_dict(self):
        """
        Converts token to dictionary.
        """
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "expires_at": self.expires_at,
        }

    @classmethod
    def from_dict(cls, dict_):
        """
        Creates token from dictionary.
        """
        return cls(**dict_)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"
