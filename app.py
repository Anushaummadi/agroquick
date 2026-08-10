from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "agroquick123"


# =========================
# HOME
# =========================

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# CONTACT
# =========================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# LOGIN
# =========================

@app.route("/login")
def login():
    return render_template("Login.html")


# =========================
# SIGNUP
# =========================

@app.route("/signup")
def signup():
    return render_template("Signup.html")


# =========================
# SEARCH + MULTILINGUAL VOICE SEARCH
# =========================

@app.route("/search")
def search():

    query = request.args.get("query", "").strip().lower()

    products = [

        {
            "name": "Rice Seeds",
            "category": "Seeds",
            "price": 100,
            "url": "/seeds"
        },

        {
            "name": "Wheat Seeds",
            "category": "Seeds",
            "price": 120,
            "url": "/seeds"
        },

        {
            "name": "Maize Seeds",
            "category": "Seeds",
            "price": 150,
            "url": "/seeds"
        },

        {
            "name": "Vegetable Seeds",
            "category": "Seeds",
            "price": 80,
            "url": "/seeds"
        },

        {
            "name": "Urea Fertilizer",
            "category": "Fertilizer",
            "price": 500,
            "url": "/fertilizer"
        },

        {
            "name": "Fertilizer",
            "category": "Fertilizer",
            "price": 450,
            "url": "/fertilizer"
        },

        {
            "name": "Water Pump",
            "category": "Equipment",
            "price": 2500,
            "url": "/equipment"
        },

        {
            "name": "Farming Tools",
            "category": "Tools",
            "price": 300,
            "url": "/tools"
        },

        {
            "name": "Plant Growth Support",
            "category": "Crop Care",
            "price": 250,
            "url": "/crop-care"
        },

        {
            "name": "Neem Based Crop Care",
            "category": "Crop Care",
            "price": 300,
            "url": "/crop-care"
        },

        {
            "name": "Micronutrient Mix",
            "category": "Crop Care",
            "price": 400,
            "url": "/crop-care"
        },

        {
            "name": "Crop Growth Booster",
            "category": "Crop Care",
            "price": 350,
            "url": "/crop-care"
        }
    ]


    # =========================
    # MULTILINGUAL SEARCH WORDS
    # =========================

    language_keywords = {

        # Seeds
        "seeds": [
            "seed",
            "seeds",
            "విత్తనాలు",
            "విత్తనం",
            "बीज",
            "बियाणे",
            "விதைகள்",
            "ಬೀಜಗಳು"
        ],

        # Fertilizer
        "fertilizer": [
            "fertilizer",
            "fertilizers",
            "ఎరువు",
            "ఎరువులు",
            "खाद",
            "उर्वरक",
            "खत",
            "உரம்",
            "ರಸಗೊಬ್ಬರ"
        ],

        # Urea
        "urea": [
            "urea",
            "యూరియా",
            "यूरिया",
            "युरिया",
            "யூரியா",
            "ಯೂರಿಯಾ"
        ],

        # Water Pump
        "water pump": [
            "water pump",
            "pump",
            "నీటి పంపు",
            "నీటి మోటార్",
            "पानी का पंप",
            "पंप",
            "पाण्याचा पंप",
            "தண்ணீர் பம்ப்",
            "ನೀರಿನ ಪಂಪ್"
        ],

        # Tools
        "tools": [
            "tool",
            "tools",
            "farming tools",
            "వ్యవసాయ పనిముట్లు",
            "పనిముట్లు",
            "कृषि उपकरण",
            "शेतीची साधने",
            "விவசாய கருவிகள்",
            "ಕೃಷಿ ಉಪಕರಣಗಳು"
        ],

        # Crop Care
        "crop care": [
            "crop care",
            "crop",
            "పంట సంరక్షణ",
            "పంట",
            "फसल देखभाल",
            "पीक संरक्षण",
            "பயிர் பராமரிப்பு",
            "ಬೆಳೆ ಆರೈಕೆ"
        ],

        # Rice
        "rice": [
            "rice",
            "rice seeds",
            "బియ్యం",
            "వరి",
            "వరి విత్తనాలు",
            "चावल",
            "धान",
            "तांदूळ",
            "भात",
            "அரிசி",
            "அரிசி விதைகள்",
            "ಅಕ್ಕಿ"
        ],

        # Wheat
        "wheat": [
            "wheat",
            "wheat seeds",
            "గోధుమ",
            "గోధుమ విత్తనాలు",
            "गेहूं",
            "गहू",
            "கோதுமை",
            "ಗೋಧಿ"
        ],

        # Maize
        "maize": [
            "maize",
            "corn",
            "maize seeds",
            "మొక్కజొన్న",
            "మొక్కజొన్న విత్తనాలు",
            "मक्का",
            "मक्याचे बियाणे",
            "மக்காச்சோளம்",
            "ಮೆಕ್ಕೆಜೋಳ"
        ]
    }


    # =========================
    # FIND SEARCH CATEGORY
    # =========================

    search_category = None

    for category, words in language_keywords.items():

        for word in words:

            if word in query:
                search_category = category
                break

        if search_category:
            break


    # =========================
    # SEARCH PRODUCTS
    # =========================

    if query:

        if search_category:

            if search_category == "seeds":

                results = [
                    product
                    for product in products
                    if product["category"].lower() == "seeds"
                ]

            elif search_category == "fertilizer":

                results = [
                    product
                    for product in products
                    if product["category"].lower() == "fertilizer"
                ]

            elif search_category == "urea":

                results = [
                    product
                    for product in products
                    if "urea" in product["name"].lower()
                ]

            elif search_category == "water pump":

                results = [
                    product
                    for product in products
                    if product["name"].lower() == "water pump"
                ]

            elif search_category == "tools":

                results = [
                    product
                    for product in products
                    if product["category"].lower() == "tools"
                ]

            elif search_category == "crop care":

                results = [
                    product
                    for product in products
                    if product["category"].lower() == "crop care"
                ]

            elif search_category == "rice":

                results = [
                    product
                    for product in products
                    if "rice" in product["name"].lower()
                ]

            elif search_category == "wheat":

                results = [
                    product
                    for product in products
                    if "wheat" in product["name"].lower()
                ]

            elif search_category == "maize":

                results = [
                    product
                    for product in products
                    if "maize" in product["name"].lower()
                ]

            else:

                results = []

        else:

            # Normal English search
            results = [
                product
                for product in products
                if query in product["name"].lower()
                or query in product["category"].lower()
            ]

    else:

        results = []


    return render_template(
        "search.html",
        query=query,
        results=results
    )


# =========================
# SEEDS
# =========================

@app.route("/seeds")
def seeds():
    return render_template("seeds.html")


# =========================
# FERTILIZER
# =========================

@app.route("/fertilizer")
def fertilizer():
    return render_template("Fertilizer.html")


# =========================
# EQUIPMENT
# =========================

@app.route("/equipment")
def equipment():
    return render_template("equipment.html")


# =========================
# TOOLS
# =========================

@app.route("/tools")
def tools():
    return render_template("tools.html")


# =========================
# CROP CARE
# =========================

@app.route("/crop-care")
def crop_care():
    return render_template("crop_care.html")


# =========================
# CART
# =========================

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


# =========================
# CHECKOUT
# =========================

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


# =========================
# ORDERS
# =========================

@app.route("/orders")
def orders():

    order = session.get("order")

    return render_template(
        "orders.html",
        order=order
    )


# =========================
# DELIVERY
# =========================

@app.route("/delivery")
def delivery():
    return render_template("Delivery.html")


# =========================
# ADD TO CART
# =========================

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():

    product = request.form.get(
        "product",
        "Product"
    )

    price = request.form.get(
        "price",
        "0"
    )

    try:

        price = float(price)

    except (ValueError, TypeError):

        price = 0


    cart_items = session.get(
        "cart",
        []
    )


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


# =========================
# INCREASE QUANTITY
# =========================

@app.route("/increase/<int:index>")
def increase(index):

    cart_items = session.get(
        "cart",
        []
    )


    if 0 <= index < len(cart_items):

        cart_items[index]["quantity"] += 1


    session["cart"] = cart_items


    return redirect("/cart")


# =========================
# DECREASE QUANTITY
# =========================

@app.route("/decrease/<int:index>")
def decrease(index):

    cart_items = session.get(
        "cart",
        []
    )


    if 0 <= index < len(cart_items):

        if cart_items[index]["quantity"] > 1:

            cart_items[index]["quantity"] -= 1

        else:

            cart_items.pop(index)


    session["cart"] = cart_items


    return redirect("/cart")


# =========================
# REMOVE FROM CART
# =========================

@app.route("/remove-from-cart/<int:index>")
def remove_from_cart(index):

    cart_items = session.get(
        "cart",
        []
    )


    if 0 <= index < len(cart_items):

        cart_items.pop(index)


    session["cart"] = cart_items


    return redirect("/cart")


# =========================
# PLACE ORDER
# =========================

@app.route("/place-order", methods=["POST"])
def place_order():

    name = request.form.get("name")

    mobile = request.form.get("mobile")

    address = request.form.get("address")


    cart_items = session.get(
        "cart",
        []
    )


    total = 0


    for item in cart_items:

        total += (
            float(item["price"])
            * int(item["quantity"])
        )


    session["order"] = {

        "name": name,

        "mobile": mobile,

        "address": address,

        "items": cart_items,

        "total": total

    }


    session["cart"] = []


    return redirect("/orders")


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )


    app.run(

        host="0.0.0.0",

        port=port

    )