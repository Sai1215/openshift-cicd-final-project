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
        product = ProductFactory(
            name="Read Product",
            description="Read description",
            price=25.50,
        )
        response = self.client.get(f"/api/products/{product.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], "Read Product")
        self.assertEqual(data["description"], "Read description")
        self.assertEqual(data["price"], 25.50)

    def test_update_product(self):
        created = self.client.post(
            "/api/products",
            json={
                "name": "Original Product",
                "description": "Original description",
                "price": 12.50,
                "category": "Books",
                "available": True,
            },
        )
        self.assertEqual(created.status_code, 201)
        original = created.get_json()
        original_id = original["id"]

        response = self.client.put(
            f"/api/products/{original_id}",
            json={"description": "Updated description"},
        )
        self.assertEqual(response.status_code, 200)
        updated = response.get_json()
        self.assertEqual(updated["id"], original_id)
        self.assertEqual(updated["description"], "Updated description")

    def test_delete_product(self):
        product = ProductFactory(name="Product to delete")
        before_count = Product.query.count()

        response = self.client.delete(f"/api/products/{product.id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(), b"")

        get_response = self.client.get(f"/api/products/{product.id}")
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(Product.query.count(), before_count - 1)

    def test_list_all_products(self):
        ProductFactory.create_batch(3)
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)

    def test_list_by_name(self):
        products = ProductFactory.create_batch(5)
        search_name = products[0].name
        response = self.client.get(
            "/api/products",
            query_string={"name": search_name},
        )
        self.assertEqual(response.status_code, 200)
        results = response.get_json()
        self.assertEqual(len(results), 1)
        for product in results:
            self.assertEqual(product["name"], search_name)

    def test_list_by_category(self):
        books = ProductFactory.create_batch(3, category="Books")
        ProductFactory.create_batch(2, category="Food")
        response = self.client.get(
            "/api/products",
            query_string={"category": "Books"},
        )
        self.assertEqual(response.status_code, 200)
        results = response.get_json()
        self.assertEqual(len(results), len(books))
        for product in results:
            self.assertEqual(product["category"], "Books")

    def test_list_by_availability(self):
        available_products = ProductFactory.create_batch(3, available=True)
        ProductFactory.create_batch(2, available=False)
        response = self.client.get(
            "/api/products",
            query_string={"available": "true"},
        )
        self.assertEqual(response.status_code, 200)
        results = response.get_json()
        self.assertEqual(len(results), len(available_products))
        for product in results:
            self.assertTrue(product["available"])


if __name__ == "__main__":
    unittest.main()
