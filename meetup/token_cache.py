"""
This module contains the TokenCache class.
"""

import logging

from .token_client import TokenClient
from .exceptions import NoCachedTokenError
from .token import Token


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
        )
        self._token = None

    @property
    def _cache_key(self):
        """
        Return the cache key for the configured client_id and redirect_uri.

        Returns:
            str: A cache key in the format
                `oauth_token_cache__<client_id>`
        """
        return f"oauth_token_cache__{self.client_id}"

    def cached_token(self):
        """
        Try to retrieve a cached token from Redis.

        Returns:
            None: Returns `None` in case of a cache miss
            Token: Returns a Token instance
        """
        logging.info("Retrieving token from Redis cache.")
        cached_token = self.redis_client.hgetall(self._cache_key)

        if not cached_token:
            logging.warning("No cached token found.")
            return None

        return Token.from_cache(cached_token)

    def _cache_token(self, token):
        """
        Persist a token in redis.

        Args:
            token (.token.Token): The token to persist.

        Returns:
            .token.Token: The persisted token.
        """
        logging.info("Persisting Token in Redis cache.")
        self.redis_client.hmset(self._cache_key, token)

        return token

    def authorize(self, code):
        """
        Initial authorization to create first API token.

        Args:
            code (str): The authorization code.

        Returns:
            Token: An instance of `Token`.
        """
        logging.info("Authorizing API client.")
        self._token = self._token_client.create_token(code=code)
        return self._token

    @property
    def token(self):
        """
        Obtains a token.
        First attempts to obtain token from memory. If no token found or token expired,
        attempts to obtain token from Redis cache. If no token found, raises
        `NoCachedTokenError`. If token expired, refreshes token. Replaces new token
        with token in memory.

        Returns:
            Token: An instance of Token

        Raises:
            NoCachedTokenError: When there is no token in Redis to refresh with.
        """
        if not self._token or self._token.expired:
            logging.debug("TokenCache._token has expired.")
            token = self.cached_token()
            if not token:
                raise NoCachedTokenError(
                    "There is no cached token. Please first run `self.authorize`."
                )
            if token.expired:
                logging.debug("Token in Redis cache has expired.")
                token = self._token_client.refresh_token(token.refresh_token)
                self._cache_token(token)
            self._token = token

        return self._token
