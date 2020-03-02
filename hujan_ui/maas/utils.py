from django.conf import settings

from requests_oauthlib import OAuth1Session, OAuth1


class MAAS:

    def __init__(self):
        self.url = settings.MAAS_URL + "api/2.0/"

    def maas_connect(self):
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
        default_headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        if headers:
            default_headers.update(headers)

        return maas.get(self.url + uri, headers=default_headers)


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
