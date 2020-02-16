"""
This module contains the TokenCache class.
"""

import logging

from .token_client import TokenClient


class TokenCache:
    """
    TokenCache

    Easily obtain and cache OAuth 2.0 token from the Meetup API.
    Obtained tokens are stored both in memory and in Redis.

    Args:
        client_id (str): The client id
        client_secret (str): The client secret
        redirect_uri (str): The redirect uri
        redis_client (redis.Redis): The Redis client

    Attributes:
        client_id (str): The client id
        client_secret (str): The client secret
        redirect_uri (str): The redirect uri
        redis_client (redis.Redis): The Redis client
    """

    def __init__(self, client_id, client_secret, redirect_uri, redis_client):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.redis_client = redis_client

        self._token_client = TokenClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            redis_client=self.redis_client,
        )
        self._token = None

    def token(self, refresh=False, code=None):
        """
        Obtain a token from cache or request a fresh token if one of the following
        conditions is true:
            * The token in the cache is expired
            * Refresh is forced

        Args:
            refresh (bool, optional): Whether to force refresh the token cache,
                defaults to `False`
            code (str, optional): Authorization code. If not `None`, will create
                new token, instead of refreshing old one.

        Returns:
            Token: An instance of Token
        """

        mode = "create" if code else "refresh"

        if refresh:
            logging.info("Refreshing token was forced.")
            self._token = self._token_client.fresh_token(mode=mode, code=code)

        if not self._token or self._token.expired:
            logging.info("TokenCache._token has expired.")
            token = self._token_client.cached_token()
            if not token or token.expired:
                logging.info("Token in Redis cache has expired.")
                token = self._token_client.fresh_token(mode=mode, code=code)
            self._token = token

        return self._token
