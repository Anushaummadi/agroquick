from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "agroquick123"


@app.route("/")
def home():
    return render_template("Home.html")


@app.route("/about")
def about():
    return render_template("About.html")


@app.route("/contact")
def contact():
    return render_template("Contact.html")


@app.route("/login")
def login():
    return render_template("Login.html")


@app.route("/signup")
def signup():
    return render_template("Signup.html")


@app.route("/search")
def search():
    return render_template("Search.html")


@app.route("/seeds")
def seeds():
    return render_template("Seeds.html")


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
        "Cart.html",
        cart=cart_items,
        total=total
    )


@app.route("/checkout")
def checkout():
    return render_template("Checkout.html")


@app.route("/orders")
def orders():
    order = session.get("order")

    return render_template(
        "Orders.html",
        order=order
    )

@app.route("/delivery")
def delivery():
    return render_template("Delivery.html")

@app.route("/add-to-cart", methods=["GET", "POST"])
def add_to_cart():

    product = request.values.get("product", "Product")
    price = request.values.get("price", "0")

    try:
        price = float(price)
    except:
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
    app.run()