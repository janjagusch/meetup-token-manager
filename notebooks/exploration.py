# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python (meetup-api-access-token-manager)
#     language: python
#     name: meetup-api-access-token-manager
# ---

import sys
import os

sys.path.append("..")

from dotenv import load_dotenv

from meetup.token_manager import TokenManager

load_dotenv()

CLIENT_ID = os.environ["MEETUP_API_KEY"]
CLIENT_SECRET = os.environ["MEETUP_API_SECRET"]
REDIRECT_URI = os.environ["MEETUP_API_REDIRECT_URI"]

token_manager = TokenManager(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI
)

token_manager.access_token

token_manager.refresh_access_token()

token_manager.access_token

token_manager.to_yaml()



ageless	Replaces the one hour expiry time from oauth2 tokens with a limit of up to two weeks
basic	Access to basic Meetup group info and creating and editing Events and RSVP's, posting photos in version 2 API's and below
event_management 	Allows the authorized application to create and make modifications to events in your Meetup groups on your behalf
group_edit 	Allows the authorized application to edit the settings of groups you organize on your behalf
group_content_edit 	Allows the authorized application to create, modify and delete group content on your behalf
group_join 	Allows the authorized application to join new Meetup groups on your behalf
messaging	Enables Member to Member messaging (this is now deprecated)
profile_edit 	Allows the authorized application to edit your profile information on your behalf
reporting	Allows the authorized application to block and unblock other members and submit abuse reports on your behalf
rsvp	Allows the authorized application to RSVP you to events on your behalf

set([1, 2]).issubset(set([1, 2, 3]))

VALID_SCOPES=[
    "ageless",
    "basic",
    "event_management",
    "group_edit",
    "group_content_edit",
    "group_join",
    "messaging",
    "profile_edit",
    "reporting",
    "rsvp"
]


def request_authorization_url(key, redirect_uri, scope=None):
    scope = set(scope or [])
    assert scope.issubset(VALID_SCOPES)
    scope = "+".join(scope)
    response_type="code"
    
    return (
        "https://secure.meetup.com/oauth2/authorize"
        f"?client_id={key}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type={response_type}"
        f"&scope={scope}"
    )


request_authorization_url(CLIENT_ID, REDIRECT_URI, scope=["ageless"])

code="3e13572cc7e6044bc5143ac1297e1eda"

token_manager = TokenManager(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI
)

token_manager.create_access_token(code=code)

token_manager.access_token

token_manager.to_yaml()
