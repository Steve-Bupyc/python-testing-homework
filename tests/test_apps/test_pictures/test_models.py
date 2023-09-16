import pytest
from factory.base import FactoryMetaClass

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture

pytestmark = pytest.mark.django_db


def test_create_favourite_picture(
    user: User, favourite_picture_data_factory: FactoryMetaClass,
) -> None:
    """Test creation favourite picture."""
    favourite_data = favourite_picture_data_factory()
    favourite_data['user'] = user
    favourite_str = (
        '<Picture {0} by {1}>'.format(
            favourite_data['foreign_id'], user.id,
        )
    )

    favourite = FavouritePicture.objects.create(**favourite_data)

    assert favourite.user == user
    assert favourite.foreign_id == favourite_data['foreign_id']
    assert favourite.url == favourite_data['url']
    assert str(favourite) == favourite_str
