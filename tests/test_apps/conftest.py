import pytest
from django.test import Client

from server.apps.identity.models import User


@pytest.fixture()
def authenticated_client(client: Client, user: User) -> Client:
    """Returns authenticated client."""
    client.force_login(user)
    return client
