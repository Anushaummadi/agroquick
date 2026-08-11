from flask import Flask, render_template, request, redirect, session
from urllib.parse import unquote
import os

app = Flask(__name__)
app.secret_key = "agroquick123"


# =========================================================
# AGROQUICK FARMING PRODUCT CATALOG
# =========================================================

PRODUCTS = [

    # =========================
    # SEEDS
    # =========================

    {
        "name": "Rice Seeds",
        "category": "Seeds",
        "price": 100,
        "url": "/seeds",
        "keywords": [
            "rice", "paddy", "rice seed", "rice seeds",
            "వరి", "వరి విత్తనాలు",
            "బియ్యం", "धान", "चावल", "तांदूळ",
            "அரிசி", "அரிசி விதைகள்", "ಅಕ್ಕಿ"
        ]
    },

    {
        "name": "Wheat Seeds",
        "category": "Seeds",
        "price": 120,
        "url": "/seeds",
        "keywords": [
            "wheat", "wheat seed", "wheat seeds",
            "గోధుమ", "గోధుమ విత్తనాలు",
            "गेहूं", "गहू", "கோதுமை", "ಗೋಧಿ"
        ]
    },

    {
        "name": "Maize Seeds",
        "category": "Seeds",
        "price": 150,
        "url": "/seeds",
        "keywords": [
            "maize", "corn", "maize seed", "maize seeds",
            "మొక్కజొన్న", "మొక్కజొన్న విత్తనాలు",
            "मक्का", "மக்காச்சோளம்", "ಮೆಕ್ಕೆಜೋಳ"
        ]
    },

    {
        "name": "Vegetable Seeds",
        "category": "Seeds",
        "price": 80,
        "url": "/seeds",
        "keywords": [
            "vegetable", "vegetables", "vegetable seeds",
            "కూరగాయలు", "కూరగాయల విత్తనాలు",
            "सब्जी", "भाजी", "காய்கறி", "ತರಕಾರಿ"
        ]
    },

    # =========================
    # FERTILIZERS
    # =========================

    {
        "name": "Urea Fertilizer",
        "category": "Fertilizer",
        "price": 500,
        "url": "/fertilizer",
        "keywords": [
            "urea", "urea fertilizer",
            "యూరియా", "यूरिया", "युरिया",
            "யூரியா", "ಯೂರಿಯಾ"
        ]
    },

    {
        "name": "General Fertilizer",
        "category": "Fertilizer",
        "price": 450,
        "url": "/fertilizer",
        "keywords": [
            "fertilizer", "fertilizers",
            "manure", "plant food",
            "ఎరువు", "ఎరువులు",
            "खाद", "उर्वरक", "खत",
            "உரம்", "ರಸಗೊಬ್ಬರ"
        ]
    },

    {
        "name": "Organic Manure",
        "category": "Fertilizer",
        "price": 350,
        "url": "/fertilizer",
        "keywords": [
            "organic manure", "manure", "organic fertilizer",
            "సేంద్రీయ ఎరువు", "సేంద్రియ ఎరువు",
            "जैविक खाद", "सेंद्रिय खत",
            "இயற்கை உரம்", "ಸಾವಯವ ಗೊಬ್ಬರ"
        ]
    },

    # =========================
    # IRRIGATION
    # =========================

    {
        "name": "Water Pump",
        "category": "Irrigation",
        "price": 2500,
        "url": "/equipment",
        "keywords": [
            "water pump", "pump", "water motor",
            "irrigation", "watering field",
            "నీటి పంపు", "నీటి మోటార్", "పారుదల",
            "पानी का पंप", "सिंचाई",
            "पाण्याचा पंप",
            "தண்ணீர் பம்ப்", "நீர்ப்பாசனம்",
            "ನೀರಿನ ಪಂಪ್"
        ]
    },

    {
        "name": "Drip Irrigation Kit",
        "category": "Irrigation",
        "price": 1800,
        "url": "/equipment",
        "keywords": [
            "drip", "drip irrigation", "irrigation kit",
            "నీటి బిందు పద్ధతి", "డ్రిప్",
            "ड्रिप सिंचाई", "ठिबक सिंचन",
            "சொட்டு நீர்", "ಹನಿ ನೀರಾವರಿ"
        ]
    },

    {
        "name": "Sprinkler Set",
        "category": "Irrigation",
        "price": 1200,
        "url": "/equipment",
        "keywords": [
            "sprinkler", "sprinkler irrigation",
            "స్ప్రింక్లర్", "స్ప్రింక్లర్ నీరుపారుదల",
            "स्प्रिंकलर", "तुषार सिंचन",
            "தெளிப்பு நீர்ப்பாசனம்",
            "ಸ್ಪ್ರಿಂಕ್ಲರ್"
        ]
    },

    # =========================
    # EQUIPMENT
    # =========================

    {
        "name": "Seed Drill",
        "category": "Equipment",
        "price": 8000,
        "url": "/equipment",
        "keywords": [
            "seed drill", "planting", "sowing",
            "seed planting", "sowing machine",
            "విత్తడం", "విత్తనాలు వేయడం",
            "बुवाई", "बीज बोना",
            "पेरणी", "விதைப்பு", "ಬಿತ್ತನೆ"
        ]
    },

    {
        "name": "Mini Cultivator",
        "category": "Equipment",
        "price": 12000,
        "url": "/equipment",
        "keywords": [
            "cultivator", "cultivation",
            "soil cultivation", "plough", "plowing",
            "నేల", "నేల సాగు",
            "मिट्टी", "जुताई",
            "माती", "नांगरणी",
            "மண்", "உழவு",
            "ಮಣ್ಣು", "ಉಳುಮೆ"
        ]
    },

    {
        "name": "Agricultural Sprayer",
        "category": "Equipment",
        "price": 3500,
        "url": "/equipment",
        "keywords": [
            "sprayer", "spraying", "spray",
            "crop spraying", "pesticide spraying",
            "స్ప్రేయర్", "పిచికారీ",
            "स्प्रे", "छिड़काव",
            "फवारणी",
            "தெளிப்பான்", "ಸಿಂಪಡಣೆ"
        ]
    },

    # =========================
    # TOOLS
    # =========================

    {
        "name": "Hand Hoe",
        "category": "Tools",
        "price": 450,
        "url": "/tools",
        "keywords": [
            "hoe", "hand hoe", "digging",
            "dig soil", "soil preparation",
            "మట్టి తవ్వడం", "మట్టి",
            "खुदाई", "मिट्टी",
            "खोदणे", "தோண்டுதல்",
            "ಮಣ್ಣು ಅಗೆಯುವುದು"
        ]
    },

    {
        "name": "Gaddapara",
        "category": "Tools",
        "price": 550,
        "url": "/tools",
        "keywords": [
            "gaddapara", "gaddapara tool",
            "digging bar", "digging tool",
            "soil digging", "dig ground",
            "గడ్డపార", "గడ్డ పార",
            "खुदाई औजार", "खोदने का औजार",
            "जमीन खोदणे"
        ]
    },

    {
        "name": "Pruning Shears",
        "category": "Tools",
        "price": 350,
        "url": "/tools",
        "keywords": [
            "pruning", "pruning shears",
            "cut branches", "trim plants",
            "కొమ్మలు కత్తిరించడం",
            "पौधे काटना", "शाखाएं काटना",
            "फांद्या कापणे",
            "கிளைகளை வெட்ட",
            "ಕೊಂಬೆಗಳನ್ನು ಕತ್ತರಿಸುವುದು"
        ]
    },

    {
        "name": "Hand Cultivator",
        "category": "Tools",
        "price": 300,
        "url": "/tools",
        "keywords": [
            "hand cultivator", "cultivator",
            "loosen soil", "soil tool",
            "మట్టి సడలించడం",
            "मिट्टी ढीली करना",
            "மண் உழவு",
            "ಮಣ್ಣನ್ನು ಸಡಿಲಿಸುವುದು"
        ]
    },

    {
        "name": "Watering Can",
        "category": "Tools",
        "price": 250,
        "url": "/tools",
        "keywords": [
            "watering can", "water plants",
            "watering",
            "మొక్కలకు నీరు", "నీరు పోయడం",
            "पानी देना",
            "रोपांना पाणी",
            "செடிகளுக்கு தண்ணீர்",
            "ಸಸ್ಯಗಳಿಗೆ ನೀರು"
        ]
    },

    # =========================
    # CROP CARE
    # =========================

    {
        "name": "Plant Growth Support",
        "category": "Crop Care",
        "price": 250,
        "url": "/crop-care",
        "keywords": [
            "plant growth", "crop growth",
            "growth support", "plant care",
            "పంట పెరుగుదల", "మొక్కల పెరుగుదల",
            "फसल वृद्धि", "पौधों की वृद्धि",
            "பயிர் வளர்ச்சி", "ಬೆಳೆ ಬೆಳವಣಿಗೆ"
        ]
    },

    {
        "name": "Neem Based Crop Care",
        "category": "Crop Care",
        "price": 300,
        "url": "/crop-care",
        "keywords": [
            "neem", "neem crop care",
            "neem based", "plant care",
            "వేప", "వేప ఆధారిత",
            "नीम", "नीम आधारित",
            "வேம்பு", "ಬೇವಿನ"
        ]
    },

    {
        "name": "Micronutrient Mix",
        "category": "Crop Care",
        "price": 400,
        "url": "/crop-care",
        "keywords": [
            "micronutrient", "micro nutrient",
            "plant nutrients", "crop nutrients",
            "సూక్ష్మ పోషకాలు",
            "सूक्ष्म पोषक तत्व",
            "सूक्ष्म अन्नद्रव्ये",
            "நுண்ணூட்டச்சத்து",
            "ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶ"
        ]
    },

    {
        "name": "Crop Growth Booster",
        "category": "Crop Care",
        "price": 350,
        "url": "/crop-care",
        "keywords": [
            "crop booster", "growth booster",
            "plant booster", "crop growth",
            "పంట బూస్టర్", "పంట పెరుగుదల",
            "फसल बूस्टर", "पीक वाढ",
            "பயிர் வளர்ச்சி",
            "ಬೆಳೆ ಬೆಳವಣಿಗೆ"
        ]
    }
]


# =========================================================
# FARMING INFORMATION
# =========================================================

FARMING_INFO = {

    "irrigation": {
        "title": "Irrigation & Water Management",
        "text": "Choose an appropriate irrigation method according to the crop, soil and field conditions."
    },

    "soil": {
        "title": "Soil & Land Preparation",
        "text": "Good soil preparation helps create suitable conditions for crop establishment and growth."
    },

    "seeds": {
        "title": "Seed Selection",
        "text": "Select suitable seeds according to the crop, season, local conditions and recommended agricultural practices."
    },

    "crop care": {
        "title": "Crop Care",
        "text": "Crop care includes appropriate watering, nutrition, weed management and monitoring for pests and diseases."
    },

    "tools": {
        "title": "Farming Tools",
        "text": "Different tools are useful for digging, soil preparation, pruning, planting and routine farm work."
    }
}


# =========================================================
# HOME
# =========================================================

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login")
def login():
    return render_template("Login.html")


# =========================================================
# SIGNUP
# =========================================================

@app.route("/signup")
def signup():
    return render_template("Signup.html")


# =========================================================
# SEARCH
# =========================================================

@app.route("/search")
def search():

    query = request.args.get("query", "").strip().lower()

    results = []

    if query:

        # ---------------------------------------------
        # Exact/keyword product search
        # ---------------------------------------------

        for product in PRODUCTS:

            searchable_text = " ".join([
                product["name"].lower(),
                product["category"].lower(),
                " ".join(product["keywords"]).lower()
            ])

            if query in searchable_text:
                results.append(product)

        # ---------------------------------------------
        # Farmer-style request matching
        # ---------------------------------------------

        request_groups = {

            "water": [
                "water", "watering", "irrigation",
                "నీరు", "నీటితో", "పారుదల",
                "पानी", "सिंचाई",
                "தண்ணீர்", "நீர்ப்பாசனம்"
            ],

            "digging": [
                "dig", "digging", "ground",
                "soil", "land preparation",
                "తవ్వ", "మట్టి", "నేల",
                "खुदाई", "मिट्टी",
                "மண்", "தோண்ட",
                "ಮಣ್ಣು", "ಅಗೆಯ"
            ],

            "planting": [
                "plant", "planting", "sowing",
                "seed", "విత్త", "నాట",
                "बुवाई", "पेरणी",
                "விதைப்பு", "ಬಿತ್ತನೆ"
            ],

            "crop": [
                "crop", "plant", "field",
                "పంట", "మొక్క",
                "फसल", "पौधा",
                "பயிர்", "சாகுபடி",
                "ಬೆಳೆ"
            ],

            "cutting": [
                "cut", "cutting", "branch",
                "prune", "trim",
                "కత్తిర", "కొమ్మ",
                "काट", "छाटणी",
                "வெட்ட",
                "ಕತ್ತರ"
            ]
        }

        matched_groups = []

        for group, words in request_groups.items():

            for word in words:

                if word in query:
                    matched_groups.append(group)
                    break

        # Add related products for farmer-style requests

        if "water" in matched_groups:
            for product in PRODUCTS:
                if product["category"] == "Irrigation" and product not in results:
                    results.append(product)

        if "digging" in matched_groups:
            for product in PRODUCTS:
                if product["category"] == "Tools" and (
                    "dig" in product["name"].lower()
                    or "hoe" in product["name"].lower()
                    or "cultivator" in product["name"].lower()
                    or "gaddapara" in product["name"].lower()
                ):
                    if product not in results:
                        results.append(product)

        if "planting" in matched_groups:
            for product in PRODUCTS:
                if (
                    product["category"] == "Seeds"
                    or "Seed Drill" in product["name"]
                ):
                    if product not in results:
                        results.append(product)

        if "crop" in matched_groups:
            for product in PRODUCTS:
                if product["category"] == "Crop Care":
                    if product not in results:
                        results.append(product)

        if "cutting" in matched_groups:
            for product in PRODUCTS:
                if "Pruning" in product["name"]:
                    if product not in results:
                        results.append(product)

    return render_template(
        "search.html",
        query=query,
        results=results
    )


# =========================================================
# FARMING INFORMATION SEARCH
# =========================================================

@app.route("/farming-info")
def farming_info():

    topic = request.args.get("topic", "").strip().lower()

    information = None

    if topic:
        for key, value in FARMING_INFO.items():
            if key in topic or topic in key:
                information = value
                break

    return render_template(
        "home.html",
        farming_info=information
    )


# =========================================================
# CATEGORY PAGES
# =========================================================

@app.route("/seeds")
def seeds():
    return render_template("seeds.html")


@app.route("/fertilizer")
def fertilizer():
    return render_template("Fertilizer.html")


@app.route("/equipment")
def equipment():
    return render_template("equipment.html")


@app.route("/tools")
def tools():
    return render_template("tools.html")


@app.route("/crop-care")
def crop_care():
    return render_template("crop_care.html")


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    total = 0

    for item in cart_items:

        total += (
            float(item["price"])
            * int(item["quantity"])
        )

    return render_template(
        "cart.html",
        cart=cart_items,
        total=total
    )


# =========================================================
# ADD TO CART - POST
# =========================================================

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

    add_product_to_cart(product, price)

    return redirect("/cart")


# =========================================================
# ADD TO CART - GET
#
# This fixes the 404 from crop-care/tools pages
# =========================================================

@app.route("/add-to-cart/<path:product>/<price>")
def add_to_cart_get(product, price):

    product = unquote(product)

    add_product_to_cart(product, price)

    return redirect("/cart")


# =========================================================
# COMMON CART FUNCTION
# =========================================================

def add_product_to_cart(product, price):

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
    session.modified = True


# =========================================================
# INCREASE QUANTITY
# =========================================================

@app.route("/increase/<int:index>")
def increase(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):

        cart_items[index]["quantity"] += 1

    session["cart"] = cart_items
    session.modified = True

    return redirect("/cart")


# =========================================================
# DECREASE QUANTITY
# =========================================================

@app.route("/decrease/<int:index>")
def decrease(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):

        if cart_items[index]["quantity"] > 1:

            cart_items[index]["quantity"] -= 1

        else:

            cart_items.pop(index)

    session["cart"] = cart_items
    session.modified = True

    return redirect("/cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

@app.route("/remove-from-cart/<int:index>")
def remove_from_cart(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):

        cart_items.pop(index)

    session["cart"] = cart_items
    session.modified = True

    return redirect("/cart")


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout")
def checkout():

    cart_items = session.get("cart", [])

    total = 0

    for item in cart_items:

        total += (
            float(item["price"])
            * int(item["quantity"])
        )

    return render_template(
        "checkout.html",
        cart=cart_items,
        total=total
    )


# =========================================================
# PLACE ORDER
# =========================================================

@app.route("/place-order", methods=["POST"])
def place_order():

    name = request.form.get("name", "").strip()
    mobile = request.form.get("mobile", "").strip()
    address = request.form.get("address", "").strip()

    cart_items = session.get("cart", [])

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


# =========================================================
# ORDERS
# =========================================================

@app.route("/orders")
def orders():

    order = session.get("order")

    return render_template(
        "orders.html",
        order=order
    )


# =========================================================
# DELIVERY
# =========================================================

@app.route("/delivery")
def delivery():

    return render_template("Delivery.html")


# =========================================================
# RUN APP
# =========================================================

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