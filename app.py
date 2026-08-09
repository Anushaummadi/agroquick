from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "agroquick123"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/login")
def login():
    return render_template("Login.html")


@app.route("/signup")
def signup():
    return render_template("Signup.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/seeds")
def seeds():
    return render_template("seeds.html")


@app.route("/fertilizer")
def fertilizer():
    return render_template("Fertilizer.html")


@app.route("/equipment")
def equipment():
    return render_template("Equipment.html")


@app.route("/tools")
def tools():
    return render_template("Tools.html")


@app.route("/crop-care")
def crop_care():
    return render_template("Crop_care.html")


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])

    total = 0

    for item in cart_items:
        total += float(item["price"]) * int(item["quantity"])

    return render_template(
        "cart.html",
        cart=cart_items,
        total=total
    )


@app.route("/checkout")
def checkout():
    cart_items = session.get("cart", [])

    total = 0

    for item in cart_items:
        total += float(item["price"]) * int(item["quantity"])

    return render_template(
        "checkout.html",
        cart=cart_items,
        total=total
    )


@app.route("/orders")
def orders():
    order = session.get("order")

    return render_template(
        "orders.html",
        order=order
    )


@app.route("/delivery")
def delivery():
    return render_template("Delivery.html")


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():

    product = request.form.get("product", "Product")
    price = request.form.get("price", "0")

    try:
        price = float(price)
    except (ValueError, TypeError):
        price = 0

    cart_items = session.get("cart", [])

    found = False

    for item in cart_items:

        if item["product"] == product:
            item["quantity"] += 1
            found = True
            break

    if not found:

        cart_items.append({
            "product": product,
            "price": price,
            "quantity": 1
        })

    session["cart"] = cart_items

    return redirect("/cart")


@app.route("/increase/<int:index>")
def increase(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):
        cart_items[index]["quantity"] += 1

    session["cart"] = cart_items

    return redirect("/cart")


@app.route("/decrease/<int:index>")
def decrease(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):

        if cart_items[index]["quantity"] > 1:
            cart_items[index]["quantity"] -= 1
        else:
            cart_items.pop(index)

    session["cart"] = cart_items

    return redirect("/cart")


@app.route("/remove-from-cart/<int:index>")
def remove_from_cart(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):
        cart_items.pop(index)

    session["cart"] = cart_items

    return redirect("/cart")


@app.route("/place-order", methods=["POST"])
def place_order():

    name = request.form.get("name")
    mobile = request.form.get("mobile")
    address = request.form.get("address")

    cart_items = session.get("cart", [])

    total = 0

    for item in cart_items:
        total += float(item["price"]) * int(item["quantity"])

    session["order"] = {
        "name": name,
        "mobile": mobile,
        "address": address,
        "items": cart_items,
        "total": total
    }

    session["cart"] = []

    return redirect("/orders")


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )