from django.conf import settings

from requests_oauthlib import OAuth1Session, OAuth1
from .exceptions import MAASError


class MAAS:
    ok = list(range(200, 205))
    fail = list(range(400, 500))

    def __init__(self):
        self.url = settings.MAAS_URL + "api/2.0/"
        self.headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

    def maas_connect(self):
        if not settings.MAAS_API_KEY:
            raise MAASError("MAAS_API_KEY not yet define")
        if not settings.MAAS_URL:
            raise MAASError("MAAS_URL not yet define")

        consumer_key, token_key, token_secret = settings.MAAS_API_KEY.split(":")
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
        if resp.status_code == 401:
            raise MAASError("MAAS API Key not valid")
        elif resp.status_code in self.fail:
            text = "Request to MAAS Server Fail"
            if settings.DEBUG:
                text += f' : {resp.text}'
            raise MAASError(text)


def maas_connect():
    consumer_key, token_key, token_secret = settings.MAAS_API_KEY.split(":")
    return OAuth1(
        consumer_key,
        client_secret='',
        resource_owner_key=token_key,
        resource_owner_secret=token_secret,
        signature_method='PLAINTEXT',
        signature_type='auth_header'
    )
