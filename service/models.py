from service import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.String(500), nullable=False, default="")
    price = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(80), nullable=False, index=True)
    available = db.Column(db.Boolean, nullable=False, default=True, index=True)

    def __repr__(self):
        return f"<Product {self.id}: {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "available": self.available,
            "availability": self.available,
        }

    @classmethod
    def create(cls, data):
        product = cls(
            name=data["name"],
            description=data.get("description", ""),
            price=float(data.get("price", 0)),
            category=data.get("category", "Uncategorized"),
            available=_to_bool(data.get("available", data.get("availability", True))),
        )
        db.session.add(product)
        db.session.commit()
        return product

    @classmethod
    def find_by_id(cls, product_id):
        return db.session.get(cls, product_id)

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(f"%{name}%")).order_by(cls.id).all()

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter(cls.category.ilike(category)).order_by(cls.id).all()

    @classmethod
    def find_by_availability(cls, available):
        return cls.query.filter_by(available=_to_bool(available)).order_by(cls.id).all()

    def update(self, data):
        if "name" in data:
            self.name = data["name"]
        if "description" in data:
            self.description = data["description"]
        if "price" in data:
            self.price = float(data["price"])
        if "category" in data:
            self.category = data["category"]
        if "available" in data or "availability" in data:
            self.available = _to_bool(data.get("available", data.get("availability")))
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "available"}
    return bool(value)
