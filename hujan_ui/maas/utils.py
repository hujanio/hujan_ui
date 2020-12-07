from django.conf import settings
from hujan_ui.installers.models import ConfigMAAS
from requests_oauthlib import OAuth1Session, OAuth1
from .exceptions import MAASError


class MAAS:
    ok = list(range(200, 205))
    fail = list(range(400, 500))
    config = ConfigMAAS.objects.first()

    def __init__(self):
        if self.config is None:
            self.url = settings.MAAS_URL + "api/2.0/"
        else:
            self.url = self.config.maas_url + "api/2.0/"
        self.headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

    def maas_connect(self):
        if self.config is None:
            if not settings.MAAS_API_KEY:
                raise MAASError("Please enter MAAS API KEY on the menu 'Settings -> MAAS Config'")
            if not settings.MAAS_URL:
                raise MAASError("Please enter MAAS URL on the menu 'Settings -> MAAS Config'")

            consumer_key, token_key, token_secret = settings.MAAS_API_KEY.split(":")
        else:
            if not self.config.maas_api_key:
                raise MAASError("Please enter MAAS API KEY on the menu 'Settings -> MAAS Config'")
            if not self.config.maas_url:
                raise MAASError("Please enter MAAS URL on the menu 'Settings -> MAAS Config'")

            consumer_key, token_key, token_secret = self.config.maas_api_key.split(":")

        return OAuth1Session(
            consumer_key,
            client_secret='',
            resource_owner_key=token_key,
            resource_owner_secret=token_secret,
            signature_method='PLAINTEXT',
            signature_type='auth_header'
        )

    def get(self, uri, params=None, headers=None):
        maas = self.maas_connect()

        if headers:
            self.headers.update(headers)
        response = maas.get(self.url + uri, params=params, headers=self.headers)
        self._validate_request(response)
        return response

    def post(self, uri, data, params=None, headers=None):
        maas = self.maas_connect()

        if headers:
            self.headers.update(headers)

        response = maas.post(self.url + uri, json=data, params=params, headers=self.headers)
        self._validate_request(response)
        return response

    def put(self, uri, data, params=None, headers=None):
        maas = self.maas_connect()

        if headers:
            self.headers.update(headers)

        response = maas.put(self.url + uri, json=data, params=params, headers=self.headers)
        self._validate_request(response)
        return response

    def delete(self, uri, params=None, headers=None):
        maas = self.maas_connect()

        if headers:
            self.headers.update(headers)

        response = maas.delete(self.url + uri, params=params, headers=self.headers)
        self._validate_request(response)
        return response

    def _validate_request(self, resp):
        if resp.status_code in self.fail:
            raise MAASError(resp.text)


def maas_connect():
    config = ConfigMAAS.objects.first()
    if config is None:
        consumer_key, token_key, token_secret = settings.MAAS_API_KEY.split(":")
    else:
        consumer_key, token_key, token_secret = config.maas_api_key.split(":")
    return OAuth1(
        consumer_key,
        client_secret='',
        resource_owner_key=token_key,
        resource_owner_secret=token_secret,
        signature_method='PLAINTEXT',
        signature_type='auth_header'
    )
