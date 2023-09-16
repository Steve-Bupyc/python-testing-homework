from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from factory.base import FactoryMetaClass

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_login_page_renders(client: Client) -> None:
    """Test page rendering with a get request."""
    response = client.get(reverse('identity:login'))

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type') == 'text/html; charset=utf-8'


@pytest.mark.django_db()
def test_invalid_login(client: Client) -> None:
    """Test that authorization doesn't allow login with invalid data."""
    response = client.post(
        reverse('identity:login'),
        data={'username': 'user', 'password': 'pass'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get('Location', '') == ''
    assert response.get('Content-Type') == 'text/html; charset=utf-8'


@pytest.mark.django_db()
def test_valid_login(
    client: Client,
    user_data_factory: FactoryMetaClass,
) -> None:
    """Test that authorization works with correct data."""
    user_data = user_data_factory()
    User.objects.create_user(**user_data)

    response = client.post(
        reverse('identity:login'),
        data={
            'username': user_data['email'],
            'password': user_data['password'],
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location', '') == reverse('pictures:dashboard')


@pytest.mark.django_db()
def test_registration_missing_required_field(
    client: Client, user_data_factory: FactoryMetaClass,
) -> None:
    """Test that registration fails with missed required fields."""
    post_data = user_data_factory(email='')
    response = client.post(
        reverse('identity:registration'),
        data=user_data_factory(),
    )

    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: dict[str, str],
    expected_user_data,
    assert_correct_user,
) -> None:
    """Test that registration works with correct data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location', '') == reverse('identity:login')

    assert_correct_user(
        registration_data['email'], expected_user_data(registration_data),
    )
