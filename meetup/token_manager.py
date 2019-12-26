"""
This module contains the TokenManager class.
"""

import requests

from .token import Token


class TokenManager:

    """
    Manages access tokens for the Meetup API.
    Can refresh and create new tokens and reads from and write into Redis.

    Args:
        client_id (str): The client id.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect uri.
        redis_client (redis.Redis): The Redis client.

    Attributes:
        client_id (str): The client id.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect uri.
        redis_client (redis.Redis): The Redis client.
    """

    def __init__(self, client_id, client_secret, redirect_uri, redis_client):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.redis_client = redis_client

    @property
    def cache_key(self):
        """
        Return the cache key for the configured client_id and redirect_uri.

        Returns:
            str: A cache key in the format
                `oauth_token_cache__<client_id>_<redirect_uri>`
        """
        return f"oauth_token_cache__{self.client_id}_{self.redirect_uri}"

    def cached_token(self):
        """
        Try to retrieve a cached token from Redis.

        Returns:
            None: Returns `None` in case of a cache miss
            Token: Returns a Token instance
        """
        cached_token = self.redis_client.hgetall(self.cache_key)

        if not cached_token:
            return None

        return Token.from_cache(cached_token)

    def cache_token(self, token):
        """
        Persist a Token instance in redis.

        Args:
            token (Token): The token to persist.

        Returns:
            Token: The persisted token.
        """

        self.redis_client.hmset(self.cache_key, token)

        return token

    def fresh_token(self, mode="refresh", code=None):
        """
        Try to create or refresh a token from the API.

        Args:
            mode (str): Either 'refresh' or 'create'.
            code (str, optional): Must be provided if mode is 'create'.

        Returns:
            Token: The fresh token.
        """
        create = mode == "create"
        url = "https://secure.meetup.com/oauth2/access"
        grant_type = "authorization_code" if create else "refresh_token"

        data = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            grant_type=grant_type,
        )

        if create:
            data["code"] = code
        else:
            data["refresh_token"] = self.cached_token().refresh_token

        response = requests.post(url=url, data=data)
        response.raise_for_status()
        response = response.json()

        token = Token.from_api(**response)

        return self.cache_token(token)
