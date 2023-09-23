import factory
from pytest_factoryboy import register

locale = 'RU_ru'


@register
class FavouritePictureDataFactory(factory.DictFactory):
    """Factory for favourite picture data."""

    foreign_id = factory.Faker('pyint', min_value=0, max_value=1000)
    url = factory.Faker('image_url')
