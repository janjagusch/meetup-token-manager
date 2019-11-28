import requests

from .access_token import AccessToken


class TokenManager:
    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        access_token=None,
        access_token_path=None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if access_token or access_token_path:
            self._access_token = access_token or AccessToken.from_yaml(
                access_token_path
            )
        else:
            self._access_token = None

    def _access(self, mode="create", code=None):
        assert mode in ("create", "refresh")
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
            data["refresh_token"] = self._access_token.refresh_token

        response = requests.post(url=url, data=data)

        return response

    def create_access_token(self, code):
        response = self._access(mode="create", code=code)
        assert response.status_code == 200

        self._access_token = AccessToken.from_api(**response.json())

    def refresh_access_token(self):
        response = self._access(mode="refresh")
        assert response.status_code == 200

        self._access_token = AccessToken.from_api(**response.json())

    def to_yaml(self, file_path="access_token.yml"):
        self.access_token.to_yaml(file_path=file_path)

    def from_yaml(self, file_path="access_token.yml"):
        self._access_token = AccessToken.from_yaml(file_path=file_path)

    @property
    def access_token(self):
        if self._access_token.expired:
            self.refresh_access_token()
        return self._access_token
