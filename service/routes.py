from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for

from service.models import Product

products_bp = Blueprint("products", __name__)


def _products_response(products):
    return jsonify([product.to_dict() for product in products])


def _availability_value(value):
    normalized = str(value).strip().lower()
    allowed = {"true", "false", "1", "0", "yes", "no", "available", "unavailable"}
    if normalized not in allowed:
        abort(400, description="Availability must be true or false.")
    return normalized in {"true", "1", "yes", "available"}


@products_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


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
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 415
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    product.update(request.get_json())
    return jsonify(product.to_dict())


@products_bp.delete("/api/products/<int:product_id>")
def delete(product_id):
    product = Product.find_by_id(product_id)
    if product is None:
        abort(404, description="Product not found.")
    product.delete()
    return "", 204


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


@products_bp.get("/")
def home():
    name = request.args.get("name", "").strip()
    category = request.args.get("category", "").strip()
    available = request.args.get("available", "").strip()
    product_id = request.args.get("product_id", "").strip()

    if product_id:
        product = Product.find_by_id(int(product_id))
        products = [product] if product else []
    elif name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available:
        products = Product.find_by_availability(_availability_value(available))
    else:
        products = Product.list_all()

    categories = sorted({item.category for item in Product.list_all()})
    flash_message = request.args.get("message", "")
    if not flash_message and any((name, category, available)):
        flash_message = "Success"

    return render_template(
        "products.html",
        products=products,
        categories=categories,
        search_name=name,
        selected_category=category,
        selected_availability=available,
        flash_message=flash_message,
    )


@products_bp.get("/products/retrieve")
def retrieve_from_ui():
    product_id = request.args.get("product_id", type=int)
    if product_id is None or Product.find_by_id(product_id) is None:
        abort(404, description="Product not found.")
    return redirect(url_for("products.home", product_id=product_id, message="Success"))


@products_bp.post("/products/update")
def update_from_ui():
    product_id = request.form.get("product_id", type=int)
    product = Product.find_by_id(product_id) if product_id else None
    if product is None:
        abort(404, description="Product not found.")
    product.update({"name": request.form.get("name", product.name)})
    return redirect(url_for("products.home", name=product.name, message="Success"))


@products_bp.post("/products/delete")
def delete_from_ui():
    product_id = request.form.get("product_id", type=int)
    product = Product.find_by_id(product_id) if product_id else None
    if product is None:
        abort(404, description="Product not found.")
    product.delete()
    return redirect(url_for("products.home", message="Success"))
