from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from factory.base import FactoryMetaClass

from server.apps.identity.models import User

pytestmark = pytest.mark.django_db


def test_unauthorized_user_update(client: Client) -> None:
    """Test page redirection with a get request from unauthorized client."""
    url = reverse('identity:user_update')

    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND
    assert (
        response.get('Location', '') ==
        '/identity/login?next=/identity/update'
    )


def test_user_update_page_renders(authenticated_client: Client) -> None:
    """Test page rendering with a get request from authenticated client."""
    response = authenticated_client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type') == 'text/html; charset=utf-8'


def test_valid_user_update(
    authenticated_client: Client,
    user: User,
    user_update_data_factory: FactoryMetaClass,
    assert_correct_user,
) -> None:
    """Test that user updates with new fields."""
    updated_data = user_update_data_factory()

    response = authenticated_client.post(
        reverse('identity:user_update'),
        data=updated_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location', '') == reverse('identity:user_update')
    assert_correct_user(user.email, updated_data)


def test_valid_user_update_without_date_of_birth(
    authenticated_client: Client,
    user: User,
    user_update_data_factory: FactoryMetaClass,
    assert_correct_user,
) -> None:
    """Test that user updates with new fields."""
    updated_data = user_update_data_factory(date_of_birth='')
    expected_data = updated_data.copy()
    expected_data['date_of_birth'] = None

    response = authenticated_client.post(
        reverse('identity:user_update'),
        data=updated_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location', '') == reverse('identity:user_update')
    assert_correct_user(user.email, expected_data)
