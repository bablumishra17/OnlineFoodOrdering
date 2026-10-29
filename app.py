
from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__)
app.secret_key = "food_ordering_project_key"

# Food Menu
FOODS = [
    {"id": 1, "name": "Veg Pizza", "price": 200, "emoji": "🍕"},
    {"id": 2, "name": "Veg Burger", "price": 100, "emoji": "🍔"},
    {"id": 3, "name": "French Fries", "price": 80, "emoji": "🍟"},
    {"id": 4, "name": "Veg Sandwich", "price": 90, "emoji": "🥪"},
    {"id": 5, "name": "White Sauce Pasta", "price": 150, "emoji": "🍝"},
    {"id": 6, "name": "Veg Biryani", "price": 160, "emoji": "🍛"},
    {"id": 7, "name": "Masala Dosa", "price": 90, "emoji": "🥞"},
    {"id": 8, "name": "Veg Momos", "price": 70, "emoji": "🥟"},
    {"id": 9, "name": "Paneer Tikka", "price": 180, "emoji": "🥘"},
    {"id": 10, "name": "Ice Cream", "price": 60, "emoji": "🍨"},
    {"id": 11, "name": "Chole Bhature", "price": 100, "emoji": "🍲"},
    {"id": 12, "name": "Paneer Roll", "price": 120, "emoji": "🌯"},
    {"id": 13, "name": "Veg Fried Rice", "price": 130, "emoji": "🍚"},
    {"id": 14, "name": "Dal Makhani", "price": 150, "emoji": "🥘"},
    {"id": 15, "name": "Gulab Jamun", "price": 50, "emoji": "🍮"},
]


def get_cart_items():
    """Convert session cart into a list of food details."""
    cart_items = []
    total = 0

    for food_id, quantity in session.get("cart", {}).items():
        food = next(
            (item for item in FOODS if item["id"] == int(food_id)),
            None
        )

        if food and quantity > 0:
            item = food.copy()
            item["quantity"] = quantity
            item["subtotal"] = item["price"] * quantity
            total += item["subtotal"]
            cart_items.append(item)

    return cart_items, total


@app.route("/")
def home():
    cart_count = sum(session.get("cart", {}).values())

    return render_template(
        "index.html",
        foods=FOODS,
        cart_count=cart_count
    )


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json(silent=True) or {}

    try:
        food_id = int(data.get("food_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid food ID"}), 400

    food = next(
        (item for item in FOODS if item["id"] == food_id),
        None
    )

    if food is None:
        return jsonify({"error": "Food item not found"}), 404

    cart = session.get("cart", {})
    key = str(food_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart

    return jsonify({
        "message": food["name"] + " added to cart!",
        "cart_count": sum(cart.values())
    })


@app.route("/api/cart/count")
def cart_count():
    count = sum(session.get("cart", {}).values())
    return jsonify({"cart_count": count})


@app.route("/cart")
def cart():
    cart_items, total = get_cart_items()

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_items, total = get_cart_items()

    if not cart_items:
        return render_template(
            "cart.html",
            cart_items=[],
            total=0
        )

    if request.method == "POST":
        customer_name = request.form.get(
            "customer_name", ""
        ).strip()

        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not customer_name or not phone or not address:
            return render_template(
                "checkout.html",
                error="Please fill in all fields.",
                cart_items=cart_items,
                total=total,
                customer_name=customer_name,
                phone=phone,
                address=address
            ), 400

        # Temporary order storage.
        # Oracle database saving will be added after DB setup.
        order = {
            "order_id": "FH" + str(__import__("time").time_ns())[-8:],
            "customer_name": customer_name,
            "phone": phone,
            "address": address,
            "items": cart_items,
            "total": total
        }

        session["last_order"] = order
        session["cart"] = {}

        return render_template(
            "order_success.html",
            order=order
        )

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total
    )


@app.route("/health")
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(debug=True)
