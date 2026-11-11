# Product Catalogue Microservice

A Flask, SQLAlchemy and Factory Boy product catalogue backend for an e-commerce application. It includes REST endpoints, unit and route tests, and Selenium/Behave BDD scenarios.

## Technology

- Python 3.10+
- Flask and Flask-SQLAlchemy
- Factory Boy and Faker for fake product data
- Nose and unittest for automated tests
- Behave, Gherkin and Selenium for BDD browser tests

## Run locally

```bash
python -m pip install -r requirements.txt
python app.py
```

The application listens on port 8000. Open http://127.0.0.1:8000/ to use the admin catalogue.

## REST API

- POST /api/products — create a product
- GET /api/products — list all products
- GET /api/products/{id} — read a product
- PUT /api/products/{id} — update a product
- DELETE /api/products/{id} — delete a product
- GET /api/products/name/{name} — find products by name
- GET /api/products/category/{category} — find products by category
- GET /api/products/availability/{true|false} — find products by availability

Product fields: name, description, price, category and available.

## Test the service

```bash
flake8 app.py service tests features
PYTHONPATH=. nosetests -v
```

## Run BDD scenarios

Install a Chrome/Chromium browser and ensure Selenium can obtain a matching driver, then run:

```bash
behave
```

BDD scenarios cover reading, updating, deleting, listing all products, and searching by name, category and availability.

## Main submission files

- tests/factories.py
- tests/test_models.py
- tests/test_routes.py
- service/routes.py
- features/steps/load_steps.py
- features/products.feature
- features/steps/web_steps.py

## GitHub Actions

The workflow at .github/workflows/workflow.yml runs flake8 and the Nose unit-test suite on pushes and pull requests to main.
