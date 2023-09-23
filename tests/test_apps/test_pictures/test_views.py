from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from factory.base import FactoryMetaClass


def test_unauthorized_dashboard(client: Client) -> None:
    """Test page redirection with a get request from unauthorized client."""
    response = client.get(reverse('pictures:dashboard'))

    assert response.status_code == HTTPStatus.FOUND
    assert (
        response.get('Location', '') ==
        '/identity/login?next=/pictures/dashboard'
    )


@pytest.mark.django_db()
def test_dashboard_page_renders(authenticated_client: Client) -> None:
    """Test page rendering with a get request from authenticated client."""
    response = authenticated_client.get(reverse('pictures:dashboard'))

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type') == 'text/html; charset=utf-8'


@pytest.mark.slow()
@pytest.mark.django_db()
def test_add_favourite(
    authenticated_client: Client,
    favourite_picture_data_factory: FactoryMetaClass,
) -> None:
    """Test adding favourite picture."""
    added_data = favourite_picture_data_factory()

    response = authenticated_client.post(
        reverse('pictures:dashboard'),
        data=added_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Content-Type') == 'text/html; charset=utf-8'


def test_unauthorized_favourites(client: Client) -> None:
    """Test page redirection with a get request from unauthorized client."""
    response = client.get(reverse('pictures:favourites'))

    assert response.status_code == HTTPStatus.FOUND
    assert (
        response.get('Location', '') ==
        '/identity/login?next=/pictures/favourites'
    )


@pytest.mark.django_db()
def test_favourites_page_renders(authenticated_client: Client) -> None:
    """Test page rendering with a get request from authenticated client."""
    response = authenticated_client.get(reverse('pictures:favourites'))

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type') == 'text/html; charset=utf-8'


@pytest.mark.slow()
@pytest.mark.timeout(5)
@pytest.mark.django_db()
@pytest.mark.usefixtures('_json_server_placeholder_api')
def test_external_service(authenticated_client: Client):
    """Test external server placeholder api for test."""
    response = authenticated_client.get(reverse('pictures:dashboard'))

    pictures = response.context['pictures']
    assert pictures
