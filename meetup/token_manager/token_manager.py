"""
This module contains a token manager that stores, loads and refreshes tokens
automatically.
"""

from meetup.token_manager.token import Token
from meetup.token_manager.token_cache import TokenCache
from meetup.token_manager.utils import refresh_token
from meetup.token_manager.exceptions import NoCachedToken


class TokenManager:
    """
    Stores, loads and refreshes tokens automatically.
    """

    def __init__(
        self, client_id, client_secret, token_cache: TokenCache, token: Token = None
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_cache = token_cache
        if token:
            self._token_cache.store_token(token)
        self._token = token

    def token(self, force_refresh=False) -> Token:
        """
        Attempts to get a valid token.
        Uses local token or loads token from token cache.
        If token is expired, refreshes token and stores new token in token cache.
        """
        token = self._token or self._token_cache.load_token()
        if not token:
            raise NoCachedToken
        if token.expired or force_refresh:
            token = refresh_token(
                self._client_id, self._client_secret, token.refresh_token
            )
            self._token_cache.store_token(token)
        self._token = token
        return self._token
