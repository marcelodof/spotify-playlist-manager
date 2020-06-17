"""Configs."""
import boto3
import json
from configs.credentials import get_credentials


def get_secrets(region_name='us-east-2'):
    """Return secrets from SecretsManager."""
    creds = get_credentials()

    session = boto3.session.Session(
        region_name=region_name,
        aws_access_key_id=creds['AWS_SECRET_KEY_ID'],
        aws_secret_access_key=creds['AWS_SECRET_ACCESS_KEY']
    )
    client = session.client(
        service_name='secretsmanager',
    )
    secrets = client.get_secret_value(
        SecretId='SpotifyClientSecrets'
    ).get('SecretString')
    spotify_configs = {
        'user': 'marcelodof',
        'scope': 'user-library-read',
        'redirect_uri': 'http://localhost:8888/callback',
    }
    return {**spotify_configs, **json.loads(secrets)}


def get_configs():
    """Return configs dict."""
    configs = {}
    spotify_secrets_configs = get_secrets()
    configs = {**configs, **spotify_secrets_configs}
    return configs
