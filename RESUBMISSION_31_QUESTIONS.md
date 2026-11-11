# Coursera Product Catalogue Final Project — Corrected Resubmission

Use the matching code block for each of the 31 text questions. Language: Python (Flask, SQLAlchemy, Factory Boy, Behave).

**Repository:** https://github.com/Sai1215/openshift-cicd-final-project

## Question 1 — ProductFactory

```python
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

```

## Question 2 — Model READ

```python
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
```

## Question 3 — Model UPDATE

```python
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
```

## Question 4 — Model DELETE

```python
def test_delete_product(self):
        product = ProductFactory(name="Product to delete")
        db.session.add(product)
        db.session.commit()
        self.assertEqual(Product.query.count(), 1)
        product.delete()
        self.assertEqual(Product.query.count(), 0)
```

## Question 5 — Model LIST ALL

```python
def test_list_all_products(self):
        self.assertEqual(Product.list_all(), [])
        ProductFactory.create_batch(3)
        self.assertEqual(len(Product.list_all()), 3)
```

## Question 6 — Model FIND BY NAME

```python
def test_find_by_name(self):
        products = ProductFactory.create_batch(5)
        search_name = products[0].name
        results = Product.find_by_name(search_name)
        self.assertGreaterEqual(len(results), 1)
        for product in results:
            self.assertEqual(product.name, search_name)
```

## Question 7 — Model FIND BY CATEGORY

```python
def test_find_by_category(self):
        books = ProductFactory.create_batch(3, category="Books")
        ProductFactory.create_batch(2, category="Food")
        results = Product.find_by_category("Books")
        self.assertEqual(len(results), len(books))
        for product in results:
            self.assertEqual(product.category, "Books")
```

## Question 8 — Model FIND BY AVAILABILITY

```python
def test_find_by_availability(self):
        available_products = ProductFactory.create_batch(3, available=True)
        ProductFactory.create_batch(2, available=False)
        results = Product.find_by_availability(True)
        self.assertEqual(len(results), len(available_products))
        for product in results:
            self.assertTrue(product.available)


if __name__ == "__main__":
    unittest.main()
```

## Question 9 — Route READ

```python
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
```

## Question 10 — Route UPDATE

```python
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
```

## Question 11 — Route DELETE

```python
def test_delete_product(self):
        product = ProductFactory(name="Product to delete")
        before_count = Product.query.count()

        response = self.client.delete(f"/api/products/{product.id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(), b"")

        get_response = self.client.get(f"/api/products/{product.id}")
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(Product.query.count(), before_count - 1)
```

## Question 12 — Route LIST ALL

```python
def test_list_all_products(self):
        ProductFactory.create_batch(3)
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)
```

## Question 13 — Route LIST BY NAME

```python
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
```

## Question 14 — Route LIST BY CATEGORY

```python
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
```

## Question 15 — Route LIST BY AVAILABILITY

```python
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
```

## Question 16 — Service READ

```python
@products_bp.get("/api/products/<int:product_id>")
def read(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    return jsonify(product.to_dict())
```

## Question 17 — Service UPDATE

```python
@products_bp.put("/api/products/<int:product_id>")
def update(product_id):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 415
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    product.update(request.get_json())
    return jsonify(product.to_dict())
```

## Question 18 — Service DELETE

```python
@products_bp.delete("/api/products/<int:product_id>")
def delete(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    product.delete()
    return "", 204
```

## Question 19 — Service LIST ALL / NAME / CATEGORY / AVAILABILITY

```python
@products_bp.get("/api/products")
def list_all():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available is not None:
        products = Product.find_by_availability(_availability_value(available))
    else:
        products = Product.list_all()

    return _products_response(products)


@products_bp.get("/api/products/name/<string:name>")
def list_by_name(name):
    return _products_response(Product.find_by_name(name))


@products_bp.get("/api/products/category/<string:category>")
def list_by_category(category):
    return _products_response(Product.find_by_category(category))


@products_bp.get("/api/products/availability/<string:availability>")
def list_by_availability(availability):
    return _products_response(
        Product.find_by_availability(_availability_value(availability))
    )
```

## Question 20 — BDD Background Data Loader

```python
import requests
from behave import given


@given("the product catalogue contains")
def load_product_data(context):
    existing = requests.get(
        f"{context.base_url}/api/products",
        timeout=10,
    )
    existing.raise_for_status()

    for product in existing.json():
        response = requests.delete(
            f"{context.base_url}/api/products/{product['id']}",
            timeout=10,
        )
        if response.status_code not in (204, 404):
            response.raise_for_status()

    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "category": row["category"],
            "available": row["available"].strip().lower() == "true",
        }
        response = requests.post(
            f"{context.base_url}/api/products",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

```

## Question 21 — BDD READ

```gherkin
Scenario: Read a product
    When I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    And I copy the product ID for "Red Apple"
    And I paste the copied ID into the "Product ID" field
    And I press the "Retrieve" button
    Then I should see "Red Apple" in the search results
    And I should see "Fresh red apple" in the search results
    And I should see "1.50" in the search results
    And I should see "Fruit" in the search results
    And I should see "Available" in the search results
```

## Question 22 — BDD UPDATE

```gherkin
Scenario: Update a product
    When I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    And I copy the product ID for "Red Apple"
    And I paste the copied ID into the "Product ID" field
    And I enter "Updated Red Apple" into the "Name" field
    And I press the "Update" button
    Then I should see the message "Success"
    When I paste the copied ID into the "Product ID" field
    And I press the "Retrieve" button
    Then I should see "Updated Red Apple" in the search results
    When I press the "Clear" button
    And I enter "Updated Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should see "Updated Red Apple" in the search results
    When I press the "Clear" button
    And I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should not see "Red Apple" in the search results
```

## Question 23 — BDD DELETE

```gherkin
Scenario: Delete a product
    When I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    And I copy the product ID for "Red Apple"
    And I paste the copied ID into the "Product ID" field
    And I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should not see "Red Apple" in the search results
```

## Question 24 — BDD LIST ALL

```gherkin
Scenario: List all products
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Red Apple" in the search results
    And I should see "Orange Juice" in the search results
```

## Question 25 — BDD SEARCH BY CATEGORY

```gherkin
Scenario: Search products by category
    When I press the "Clear" button
    And I select "Drinks" from the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Orange Juice" in the search results
    And I should see "Green Tea" in the search results
    And I should not see "Red Apple" in the search results
```

## Question 26 — BDD SEARCH BY AVAILABILITY

```gherkin
Scenario: Search products by availability
    When I press the "Clear" button
    And I select "Available" from the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Red Apple" in the search results
    And I should see "Green Tea" in the search results
    And I should not see "Orange Juice" in the search results
```

## Question 27 — BDD SEARCH BY NAME

```gherkin
Scenario: Search products by name
    When I press the "Clear" button
    And I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Red Apple" in the search results
    And I should not see "Orange Juice" in the search results
```

## Question 28 — BDD Button Press

```python
@when('I press the "{button}" button')
def press_button(context, button):
    context.driver.find_element(
        By.XPATH,
        f'//button[normalize-space()="{button}"]',
    ).click()
```

## Question 29 — Verify Text Is Present in Search Results

```python
@then('I should see "{text}" in the search results')
def verify_text_present(context, text):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert text in results.text, f"Expected '{text}' in search results: {results.text}"
```

## Question 30 — Verify Text Is Absent from Search Results

```python
@then('I should not see "{text}" in the search results')
def verify_text_absent(context, text):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert text not in results.text, f"Did not expect '{text}' in search results: {results.text}"
```

## Question 31 — Verify Message Is Present

```python
@then('I should see the message "{message}"')
def see_message(context, message):
    flash_message = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash_message"))
    )
    assert message in flash_message.text
```

