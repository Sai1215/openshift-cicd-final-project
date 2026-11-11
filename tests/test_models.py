import unittest

from app import app
from service import db
from service.models import Product
from tests.factories import ProductFactory


class ProductModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()

    def test_read_product(self):
        created = ProductFactory(name="Read Product")
        found = Product.find_by_id(created.id)
        self.assertEqual(found.name, "Read Product")

    def test_update_product(self):
        product = ProductFactory(name="Old Product")
        product.update({"name": "Updated Product", "price": 42.5})
        found = Product.find_by_id(product.id)
        self.assertEqual(found.name, "Updated Product")
        self.assertEqual(found.price, 42.5)

    def test_delete_product(self):
        product = ProductFactory()
        product_id = product.id
        product.delete()
        self.assertIsNone(Product.find_by_id(product_id))

    def test_list_all_products(self):
        ProductFactory.create_batch(3)
        self.assertEqual(len(Product.list_all()), 3)

    def test_find_by_name(self):
        ProductFactory(name="Sapphire Phone")
        ProductFactory(name="Desk Lamp")
        results = Product.find_by_name("sapphire")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Sapphire Phone")

    def test_find_by_category(self):
        ProductFactory(category="Books")
        ProductFactory(category="Food")
        results = Product.find_by_category("Books")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, "Books")

    def test_find_by_availability(self):
        ProductFactory(available=True)
        ProductFactory(available=False)
        results = Product.find_by_availability(True)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].available)


if __name__ == "__main__":
    unittest.main()
