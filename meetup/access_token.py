import time

import requests

from .utils import read_yaml, write_yaml


class AccessToken:
    """
    An access token for the Meetup API that is aware of its expiry data.

    Args:
        access_token (str): The access token.
        token_token (str): The token type.
        lifetime (int): Total number of seconds token will be alive.
        expires_at (int): Unix timestamp when token will expire.
        refresh_token (str): The refresh token.

    Attributes:
        access_token (str): The access token.
        token_token (str): The token type.
        lifetime (int): Total number of seconds token will be alive.
        expires_at (int): Unix timestamp when token will expire.
        refresh_token (str): The refresh token.
    """

    def __init__(
        self, *, access_token, token_type, lifetime, expires_at, refresh_token
    ):
        self.access_token = access_token
        self.token_type = token_type
        self.lifetime = lifetime
        self.expires_at = expires_at
        self.refresh_token = refresh_token

    @classmethod
    def from_api(cls, access_token, expires_in, token_type, refresh_token):
        """
        Initializes a fresh token from the API.

        Args:
            access_token (str): The access token.
            expires_in (int): Total number of seconds until token will expire. This
                assumes that the token has been created now.
            token_type (str): The token type.
            refresh_token (str): The refresh token.

        Returns:
            AccesToken: An instance of AccessToken.
        """
        expires_at = int(time.time()) + expires_in

        return cls(
            access_token=access_token,
            lifetime=expires_in,
            expires_at=expires_at,
            token_type=token_type,
            refresh_token=refresh_token,
        )

    @staticmethod
    def from_yaml(file_path="access_token.yml"):
        """
        Retrieves token from yaml file.

        Args:
            file_path (str): File path to the AccessToken object.

        Returns:
            AccessToken: An instance of AccessToken.
        """
        return read_yaml(file_path)

    def to_yaml(self, file_path="access_token.yml"):
        """
        Writes token to yaml file.

        Args:
            file_path (str): File path where AccessToken instance should be stored.
        """
        write_yaml(self, file_path)

    @property
    def expired(self):
        """
        Checks whether or not the access token has expired.

        Returns:
            bool: Whether or not the access token has expired.
        """
        return int(time.time()) > self.expires_at

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            "("
            f"access_token={self.access_token},"
            f"token_type={self.token_type},"
            f"refresh_token={self.refresh_token},"
            f"lifetime={self.lifetime},"
            f"expires_at={self.expires_at}"
            ")"
        )
