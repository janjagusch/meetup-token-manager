"""
This module contains the token caches.
"""

from typing import Dict
import abc
import json
import logging

from google.cloud import storage
import redis

from meetup.token_manager.token import Token


class TokenCache(abc.ABC):
    """
    Abstract token cache base class.
    """

    def store_token(self, token: Token):
        """
        Stores the token in the cache.
        """
        logging.debug("Storing token.")
        self._store_token(token.to_dict())

    def load_token(self) -> Token:
        """
        Loads the token from the cache.
        """
        logging.debug("Loading token.")
        return Token.from_dict(self._load_token())

    @abc.abstractmethod
    def _store_token(self, token: Dict):
        raise NotImplementedError

    @abc.abstractmethod
    def _load_token(self) -> Dict:
        raise NotImplementedError


class TokenCacheRedis(TokenCache):
    """
    Stores and loads tokens in Redis.
    """

    def __init__(self, redis_client: redis.Redis, redis_key: str = "token"):
        self._redis_client = redis_client
        self._redis_key = redis_key

    def _store_token(self, token):
        self._redis_client.hmset(self._redis_key, token)

    def _load_token(self):
        return self._redis_client.hgetall(self._redis_key)


class TokenCacheFile(TokenCache):
    """
    Stores and loads tokens from the filesystem.
    """

    def __init__(self, filepath: str = "token.json"):
        self._filepath = filepath

    def _store_token(self, token):
        with open(self._filepath, mode="w") as file_pointer:
            json.dump(token, file_pointer)

    def _load_token(self):
        with open(self._filepath, mode="r") as file_pointer:
            return json.load(file_pointer)


class TokenCacheGCS(TokenCache):
    """
    Stores and loads tokens from Google Cloud Storage.
    """

    def __init__(self, bucket_name: str, blob_name: str = "token.json"):
        self._bucket_name = bucket_name
        self._blob_name = blob_name

    @property
    def bucket_name(self):
        """
        bucket_name
        """
        return self._bucket_name

    @property
    def blob_name(self):
        """
        blob_name
        """
        return self._blob_name

    @property
    def _blob(self):
        client = storage.Client()
        bucket = client.bucket(self.bucket_name)
        return bucket.blob(self.blob_name)

    def _load_token(self):
        return json.loads(self._blob.download_as_string())

    def _store_token(self, token):
        self._blob.upload_from_string(json.dumps(token))
