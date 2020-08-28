"""
Custom exceptions.
"""


class MeetupTokenCacheError(Exception):
    """
	Base exception for this package.
	"""


class TokenClientError(MeetupTokenCacheError):
    """
	Error when something goes wrong with the `TokenClient` class.
	"""


class NoCachedTokenError(TokenClientError):
    """
	Error when attempting to obtain cached Redis token that does not exist.
	"""
