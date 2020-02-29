from django.conf import settings

from requests_oauthlib import OAuth1Session, OAuth1



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
