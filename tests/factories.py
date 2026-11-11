import factory
from factory.alchemy import SQLAlchemyModelFactory

from service import db
from service.models import Product


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda number: number + 1)
    name = factory.Sequence(lambda number: f"Product {number}")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    category = factory.Iterator(["Electronics", "Books", "Food", "Clothing"])
    available = factory.Faker("boolean")


def fake_products(count=5):
    return ProductFactory.create_batch(count)
