# Product Catalogue Microservice

A Python Flask and SQLAlchemy product catalogue backend for an e-commerce application, with Factory Boy fakes, model and route tests, and Selenium/Behave BDD scenarios.

## Run

```bash
python -m pip install -r requirements.txt
python app.py
```

The application runs on port 8000 at http://127.0.0.1:8000/.

## REST API

- `POST /api/products` — create a product from a JSON payload.
- `GET /api/products` — list products; optional query parameters are `name`, `category`, or `available`.
- `GET /api/products/{id}` — read a product.
- `PUT /api/products/{id}` — update a product. Send JSON content type.
- `DELETE /api/products/{id}` — delete a product (204 No Content).
 
Product fields are `id`, `name`, `description`, `price`, `category`, and `available`.

## Automated tests

```bash
flake8 app.py service tests features
PYTHONPATH=. nosetests -v
```

## BDD browser scenarios

Install Chrome/Chromium and ensure Selenium can launch a matching driver:

```bash
behave
```

The Behave feature covers product read, update, delete, list all, and search by name, category, and availability. Background data is loaded through the Product API using POST requests.

## Submission files

- `tests/factories.py`
- `tests/test_models.py`
- `tests/test_routes.py`
- `service/routes.py`
- `features/steps/load_steps.py`
- `features/products.feature`
- `features/steps/web_steps.py`
