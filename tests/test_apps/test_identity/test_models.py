import pytest
from factory.base import FactoryMetaClass

from server.apps.identity.models import User

pytestmark = pytest.mark.django_db


def test_create_user(
    user_data_factory: FactoryMetaClass,
    expected_user_data,
    assert_correct_user,
) -> None:
    """Test creation user."""
    user_data = user_data_factory()

    User.objects.create_user(**user_data)

    assert_correct_user(user_data['email'], expected_user_data(user_data))


def test_create_superuser(
    user_data_factory: FactoryMetaClass,
    expected_user_data,
    assert_correct_superuser,
) -> None:
    """Test creation superuser."""
    user_data = user_data_factory()

    User.objects.create_superuser(**user_data)

    assert_correct_superuser(user_data['email'], expected_user_data(user_data))


def test_create_user_missing_email(
    user_data_factory: FactoryMetaClass,
) -> None:
    """Test creation user fails with missed required field."""
    user_data = user_data_factory(email='')

    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_user(**user_data)

    assert not User.objects.filter(email=user_data['email']).exists()
