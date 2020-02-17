"""
Helper functions for the `.token_cache` package.
"""


def make_authorization_url(client_id, redirect_uri, scope=None):
    """
    Generates an authorization url for the Meetup API.

    Args:
        client_id (str): The key of your consumer.
        redirect_uri (str): The redirect uri of your consumer.
        scope (list): A list of scopes you want to give to the consumer. More
            information about scopes here: https://www.meetup.com/meetup_api/auth/.

    Returns:
        str: The url you need to visit to authorize the consumer.

    Raises:
        KeyError: When providing invalid scopes.    
    """
    scope = set(scope or [])
    VALID_SCOPES = [
        "ageless",
        "basic",
        "event_management",
        "group_edit",
        "group_content_edit",
        "group_join",
        "messaging",
        "profile_edit",
        "reporting",
        "rsvp",
    ]
    if not scope.issubset(VALID_SCOPES):
        raise ValueError(f"Scope '{scope}' is not a subset of '{_VALID_SCOPES}'")

    scope = "+".join(scope)
    response_type = "code"

    return (
        "https://secure.meetup.com/oauth2/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type={response_type}"
        f"&scope={scope}"
    )
