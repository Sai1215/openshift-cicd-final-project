import unittest

from app import app
from service import db
from service.models import Product
from tests.factories import ProductFactory


class ProductRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()

    def test_read_product(self):
        product = ProductFactory(name="Read Product")
        response = self.client.get(f"/api/products/{product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Read Product")

    def test_update_product(self):
        product = ProductFactory(name="Old Product")
        response = self.client.put(
            f"/api/products/{product.id}",
            json={"name": "Updated Product"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated Product")

    def test_delete_product(self):
        product = ProductFactory()
        response = self.client.delete(f"/api/products/{product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Product.find_by_id(product.id))

    def test_list_all_products(self):
        ProductFactory.create_batch(3)
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)

    def test_list_by_name(self):
        ProductFactory(name="Sapphire Phone")
        ProductFactory(name="Desk Lamp")
        response = self.client.get("/api/products/name/sapphire")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["name"] for item in response.get_json()], ["Sapphire Phone"])

    def test_list_by_category(self):
        ProductFactory(category="Books")
        ProductFactory(category="Food")
        response = self.client.get("/api/products/category/Books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]["category"], "Books")

    def test_list_by_availability(self):
        ProductFactory(available=True)
        ProductFactory(available=False)
        response = self.client.get("/api/products/availability/true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertTrue(response.get_json()[0]["available"])


if __name__ == "__main__":
    unittest.main()
