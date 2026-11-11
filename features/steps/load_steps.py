from behave import given

from app import app
from service import db
from service.models import Product


@given("the product catalogue contains")
def load_product_data(context):
    with app.app_context():
        db.session.query(Product).delete()
        db.session.commit()

        for row in context.table:
            product = Product(
                name=row["name"],
                description=row["description"],
                price=float(row["price"]),
                category=row["category"],
                available=row["available"].strip().lower() == "true",
            )
            db.session.add(product)

        db.session.commit()
