"""
Custom exceptions.
"""


class MeetupTokenManagerError(Exception):
    """
	Base exception for this package.
	"""


class NoCachedToken(MeetupTokenManagerError):
    """
	Error when no cached token can be found.
	"""
