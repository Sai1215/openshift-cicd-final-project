from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for

from service.models import Product

products_bp = Blueprint("products", __name__)


def _products_response(products):
    return jsonify([product.to_dict() for product in products])


def _availability_value(value):
    normalized = value.strip().lower()
    if normalized not in {"true", "false", "1", "0", "yes", "no", "available", "unavailable"}:
        abort(400, description="Availability must be true or false.")
    return normalized in {"true", "1", "yes", "available"}


@products_bp.post("/api/products")
def create():
    data = request.get_json(silent=True) or {}
    if not data.get("name"):
        return jsonify({"error": "Product name is required."}), 400
    product = Product.create(data)
    return jsonify(product.to_dict()), 201


@products_bp.get("/api/products/<int:product_id>")
def read(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    return jsonify(product.to_dict())


@products_bp.put("/api/products/<int:product_id>")
def update(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    product.update(request.get_json(silent=True) or {})
    return jsonify(product.to_dict())


@products_bp.delete("/api/products/<int:product_id>")
def delete(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    product.delete()
    return jsonify({"deleted": product_id})


@products_bp.get("/api/products")
def list_all():
    return _products_response(Product.list_all())


@products_bp.get("/api/products/name/<string:name>")
def list_by_name(name):
    return _products_response(Product.find_by_name(name))


@products_bp.get("/api/products/category/<string:category>")
def list_by_category(category):
    return _products_response(Product.find_by_category(category))


@products_bp.get("/api/products/availability/<string:availability>")
def list_by_availability(availability):
    return _products_response(Product.find_by_availability(_availability_value(availability)))


@products_bp.get("/")
def home():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    availability = request.args.get("availability", "").strip()

    products = Product.find_by_name(query) if query else Product.list_all()
    if category:
        products = [item for item in products if item.category.lower() == category.lower()]
    if availability in {"true", "false"}:
        expected = availability == "true"
        products = [item for item in products if item.available is expected]

    categories = sorted({item.category for item in Product.list_all()})
    return render_template(
        "products.html",
        products=products,
        categories=categories,
        query=query,
        selected_category=category,
        selected_availability=availability,
    )


@products_bp.get("/products/<int:product_id>")
def detail(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404)
    return render_template("product_detail.html", product=product)


@products_bp.post("/products/<int:product_id>/edit")
def update_from_ui(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404)
    product.update(request.form)
    return redirect(url_for("products.detail", product_id=product.id))


@products_bp.post("/products/<int:product_id>/delete")
def delete_from_ui(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404)
    product.delete()
    return redirect(url_for("products.home"))
