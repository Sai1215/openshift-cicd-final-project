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
        created = ProductFactory(
            name="Read Product",
            description="Product description",
            price=19.95,
        )
        found = Product.find_by_id(created.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, created.id)
        self.assertEqual(found.name, "Read Product")
        self.assertEqual(found.description, "Product description")
        self.assertEqual(found.price, 19.95)

    def test_update_product(self):
        product = ProductFactory(
            name="Original Product",
            description="Original description",
        )
        original_id = product.id
        product.update({"description": "Updated description"})
        found = Product.find_by_id(original_id)
        self.assertEqual(found.id, original_id)
        self.assertEqual(found.description, "Updated description")

    def test_delete_product(self):
        product = ProductFactory(name="Product to delete")
        db.session.add(product)
        db.session.commit()
        self.assertEqual(Product.query.count(), 1)
        product.delete()
        self.assertEqual(Product.query.count(), 0)

    def test_list_all_products(self):
        self.assertEqual(Product.list_all(), [])
        ProductFactory.create_batch(3)
        self.assertEqual(len(Product.list_all()), 3)

    def test_find_by_name(self):
        products = ProductFactory.create_batch(5)
        search_name = products[0].name
        results = Product.find_by_name(search_name)
        self.assertGreaterEqual(len(results), 1)
        for product in results:
            self.assertEqual(product.name, search_name)

    def test_find_by_category(self):
        books = ProductFactory.create_batch(3, category="Books")
        ProductFactory.create_batch(2, category="Food")
        results = Product.find_by_category("Books")
        self.assertEqual(len(results), len(books))
        for product in results:
            self.assertEqual(product.category, "Books")

    def test_find_by_availability(self):
        available_products = ProductFactory.create_batch(3, available=True)
        ProductFactory.create_batch(2, available=False)
        results = Product.find_by_availability(True)
        self.assertEqual(len(results), len(available_products))
        for product in results:
            self.assertTrue(product.available)


if __name__ == "__main__":
    unittest.main()
