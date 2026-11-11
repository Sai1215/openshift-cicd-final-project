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
