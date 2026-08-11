from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "agroquick123"


# =========================================================
# AGROQUICK PRODUCT CATALOGUE
# =========================================================

PRODUCTS = [

    # =====================================================
    # 1. SEEDS
    # =====================================================

    {"name": "Rice Seeds", "category": "Seeds", "price": 100, "url": "/seeds",
     "keywords": ["rice", "paddy", "వరి", "వరి విత్తనాలు", "धान"]},

    {"name": "Wheat Seeds", "category": "Seeds", "price": 120, "url": "/seeds",
     "keywords": ["wheat", "గోధుమ", "गहू", "गेहूं"]},

    {"name": "Maize Seeds", "category": "Seeds", "price": 150, "url": "/seeds",
     "keywords": ["maize", "corn", "మొక్కజొన్న", "मक्का"]},

    {"name": "Cotton Seeds", "category": "Seeds", "price": 180, "url": "/seeds",
     "keywords": ["cotton", "పత్తి", "कपास"]},

    {"name": "Groundnut Seeds", "category": "Seeds", "price": 140, "url": "/seeds",
     "keywords": ["groundnut", "peanut", "వేరుశెనగ", "मूंगफली"]},

    {"name": "Sunflower Seeds", "category": "Seeds", "price": 130, "url": "/seeds",
     "keywords": ["sunflower", "సూర్యకాంతి", "सूरजमुखी"]},

    {"name": "Soybean Seeds", "category": "Seeds", "price": 160, "url": "/seeds",
     "keywords": ["soybean", "soy", "సోయాబీన్", "सोयाबीन"]},

    {"name": "Chilli Seeds", "category": "Seeds", "price": 90, "url": "/seeds",
     "keywords": ["chilli", "chili", "మిరప", "మిరపకాయ", "मिर्च"]},

    {"name": "Tomato Seeds", "category": "Seeds", "price": 85, "url": "/seeds",
     "keywords": ["tomato", "టమాట", "टमाटर"]},

    {"name": "Brinjal Seeds", "category": "Seeds", "price": 80, "url": "/seeds",
     "keywords": ["brinjal", "eggplant", "వంకాయ", "बैंगन"]},

    {"name": "Okra Seeds", "category": "Seeds", "price": 75, "url": "/seeds",
     "keywords": ["okra", "lady finger", "బెండకాయ", "भिंडी"]},

    {"name": "Onion Seeds", "category": "Seeds", "price": 95, "url": "/seeds",
     "keywords": ["onion", "ఉల్లి", "प्याज"]},

    {"name": "Vegetable Seeds Mix", "category": "Seeds", "price": 150, "url": "/seeds",
     "keywords": ["vegetable seeds", "vegetables", "కూరగాయల విత్తనాలు"]},


    # =====================================================
    # 2. FERTILIZERS & MANURE
    # =====================================================

    {"name": "Urea Fertilizer", "category": "Fertilizer", "price": 500,
     "url": "/fertilizer", "keywords": ["urea", "యూరియా", "यूरिया"]},

    {"name": "DAP Fertilizer", "category": "Fertilizer", "price": 650,
     "url": "/fertilizer", "keywords": ["dap", "dap fertilizer", "డిఏపి"]},

    {"name": "NPK Fertilizer", "category": "Fertilizer", "price": 700,
     "url": "/fertilizer", "keywords": ["npk", "npk fertilizer", "ఎన్పీకే"]},

    {"name": "Potash Fertilizer", "category": "Fertilizer", "price": 550,
     "url": "/fertilizer", "keywords": ["potash", "పొటాష్"]},

    {"name": "Organic Manure", "category": "Fertilizer", "price": 350,
     "url": "/fertilizer", "keywords": ["manure", "organic manure", "సేంద్రీయ ఎరువు"]},

    {"name": "Vermicompost", "category": "Fertilizer", "price": 400,
     "url": "/fertilizer", "keywords": ["vermicompost", "వర్మీకంపోస్ట్"]},

    {"name": "Compost Fertilizer", "category": "Fertilizer", "price": 300,
     "url": "/fertilizer", "keywords": ["compost", "కంపోస్ట్"]},

    {"name": "Micronutrient Fertilizer", "category": "Fertilizer", "price": 450,
     "url": "/fertilizer", "keywords": ["micronutrient", "micro nutrient", "సూక్ష్మ పోషకాలు"]},


    # =====================================================
    # 3. HAND TOOLS
    # =====================================================

    {"name": "Gaddapara", "category": "Tools", "price": 550,
     "url": "/tools",
     "keywords": [
         "gaddapara", "gaddapara tool", "digging bar",
         "digging tool", "dig soil", "dig ground",
         "గడ్డపార", "గడ్డ పార", "గడ్డపారా",
         "खुदाई औजार"
     ]},

    {"name": "Spade", "category": "Tools", "price": 450,
     "url": "/tools",
     "keywords": ["spade", "digging spade", "soil digging", "గడ్డపార", "फावड़ा"]},

    {"name": "Shovel", "category": "Tools", "price": 500,
     "url": "/tools",
     "keywords": ["shovel", "digging", "soil", "మట్టి తవ్వడం"]},

    {"name": "Hand Hoe", "category": "Tools", "price": 450,
     "url": "/tools",
     "keywords": ["hoe", "hand hoe", "dig", "digging", "మట్టి తవ్వడం"]},

    {"name": "Pickaxe", "category": "Tools", "price": 650,
     "url": "/tools",
     "keywords": ["pickaxe", "pick axe", "dig hard soil", "గునపం"]},

    {"name": "Sickle", "category": "Tools", "price": 300,
     "url": "/tools",
     "keywords": ["sickle", "harvesting", "grass cutting", "కొడవలి", "हंसिया"]},

    {"name": "Axe", "category": "Tools", "price": 700,
     "url": "/tools",
     "keywords": ["axe", "wood cutting", "కత్తి", "कुल्हाड़ी"]},

    {"name": "Pruning Shears", "category": "Tools", "price": 350,
     "url": "/tools",
     "keywords": ["pruning", "shears", "cut branches", "trim plants"]},

    {"name": "Garden Rake", "category": "Tools", "price": 400,
     "url": "/tools",
     "keywords": ["rake", "garden rake", "soil leveling"]},

    {"name": "Garden Fork", "category": "Tools", "price": 450,
     "url": "/tools",
     "keywords": ["garden fork", "fork", "soil"]},

    {"name": "Hand Trowel", "category": "Tools", "price": 180,
     "url": "/tools",
     "keywords": ["trowel", "hand trowel", "planting"]},

    {"name": "Hand Weeder", "category": "Tools", "price": 220,
     "url": "/tools",
     "keywords": ["weeder", "weed removal", "weeding", "కలుపు"]},

    {"name": "Hand Cultivator", "category": "Tools", "price": 300,
     "url": "/tools",
     "keywords": ["hand cultivator", "cultivator", "soil loosening"]},

    {"name": "Watering Can", "category": "Tools", "price": 250,
     "url": "/tools",
     "keywords": ["watering can", "water plants", "watering"]},

    {"name": "Wheelbarrow", "category": "Tools", "price": 2200,
     "url": "/tools",
     "keywords": ["wheelbarrow", "farm transport", "carry soil"]},


    # =====================================================
    # 4. FARM MACHINERY
    # =====================================================

    {"name": "Mini Cultivator", "category": "Machinery", "price": 12000,
     "url": "/equipment",
     "keywords": ["cultivator", "cultivation", "plough", "plowing"]},

    {"name": "Power Tiller", "category": "Machinery", "price": 65000,
     "url": "/equipment",
     "keywords": ["power tiller", "tiller", "farm machine"]},

    {"name": "Seed Drill Machine", "category": "Machinery", "price": 8000,
     "url": "/equipment",
     "keywords": ["seed drill", "sowing machine", "planting machine"]},

    {"name": "Agricultural Sprayer", "category": "Machinery", "price": 3500,
     "url": "/equipment",
     "keywords": ["sprayer", "spray", "crop spraying"]},

    {"name": "Battery Sprayer", "category": "Machinery", "price": 4500,
     "url": "/equipment",
     "keywords": ["battery sprayer", "sprayer", "spraying"]},

    {"name": "Brush Cutter", "category": "Machinery", "price": 9000,
     "url": "/equipment",
     "keywords": ["brush cutter", "grass cutter", "weed cutter"]},

    {"name": "Chaff Cutter", "category": "Machinery", "price": 15000,
     "url": "/equipment",
     "keywords": ["chaff cutter", "fodder cutter"]},


    # =====================================================
    # 5. IRRIGATION
    # =====================================================

    {"name": "Water Pump", "category": "Irrigation", "price": 2500,
     "url": "/equipment",
     "keywords": ["water pump", "pump", "water motor", "irrigation"]},

    {"name": "Drip Irrigation Kit", "category": "Irrigation", "price": 1800,
     "url": "/equipment",
     "keywords": ["drip", "drip irrigation", "irrigation kit"]},

    {"name": "Sprinkler Set", "category": "Irrigation", "price": 1200,
     "url": "/equipment",
     "keywords": ["sprinkler", "sprinkler irrigation"]},

    {"name": "Agricultural Water Pipe", "category": "Irrigation", "price": 900,
     "url": "/equipment",
     "keywords": ["water pipe", "farm pipe", "irrigation pipe"]},

    {"name": "Garden Hose", "category": "Irrigation", "price": 600,
     "url": "/equipment",
     "keywords": ["hose", "water hose", "watering"]},


    # =====================================================
    # 6. CROP CARE
    # =====================================================

    {"name": "Crop Growth Booster", "category": "Crop Care", "price": 350,
     "url": "/crop-care",
     "keywords": ["growth booster", "crop growth", "plant growth"]},

    {"name": "Neem Based Crop Care", "category": "Crop Care", "price": 300,
     "url": "/crop-care",
     "keywords": ["neem", "neem crop care", "plant care"]},

    {"name": "Plant Nutrient Mix", "category": "Crop Care", "price": 400,
     "url": "/crop-care",
     "keywords": ["plant nutrients", "crop nutrients", "nutrient mix"]},

    {"name": "Bio Crop Care", "category": "Crop Care", "price": 450,
     "url": "/crop-care",
     "keywords": ["bio", "bio crop care", "organic crop care"]},

    {"name": "Plant Growth Support", "category": "Crop Care", "price": 250,
     "url": "/crop-care",
     "keywords": ["plant growth", "crop care"]},


    # =====================================================
    # 7. FARM ACCESSORIES
    # =====================================================

    {"name": "Seedling Tray", "category": "Farm Accessories", "price": 120,
     "url": "/equipment",
     "keywords": ["seedling tray", "nursery tray", "seed tray"]},

    {"name": "Plant Support Sticks", "category": "Farm Accessories", "price": 180,
     "url": "/equipment",
     "keywords": ["plant support", "support sticks", "plant sticks"]},

    {"name": "Agricultural Rope", "category": "Farm Accessories", "price": 250,
     "url": "/equipment",
     "keywords": ["rope", "farm rope", "agriculture rope"]},

    {"name": "Harvest Basket", "category": "Farm Accessories", "price": 350,
     "url": "/equipment",
     "keywords": ["basket", "harvest basket", "harvesting"]},

    {"name": "Plastic Crate", "category": "Farm Accessories", "price": 450,
     "url": "/equipment",
     "keywords": ["crate", "farm crate", "storage"]},


    # =====================================================
    # 8. STORAGE
    # =====================================================

    {"name": "Grain Storage Bag", "category": "Storage", "price": 120,
     "url": "/equipment",
     "keywords": ["grain bag", "storage bag", "grain storage"]},

    {"name": "Seed Storage Container", "category": "Storage", "price": 250,
     "url": "/equipment",
     "keywords": ["seed storage", "seed container", "storage"]},

    {"name": "Grain Storage Container", "category": "Storage", "price": 600,
     "url": "/equipment",
     "keywords": ["grain container", "grain storage"]},


    # =====================================================
    # 9. NURSERY & GARDEN
    # =====================================================

    {"name": "Plant Pots", "category": "Nursery", "price": 150,
     "url": "/tools",
     "keywords": ["pots", "plant pots", "nursery"]},

    {"name": "Seedling Grow Bags", "category": "Nursery", "price": 200,
     "url": "/tools",
     "keywords": ["grow bags", "seedling bags", "nursery"]},

    {"name": "Garden Net", "category": "Nursery", "price": 500,
     "url": "/equipment",
     "keywords": ["garden net", "plant net", "crop net"]},


    # =====================================================
    # 10. SOIL PREPARATION
    # =====================================================

    {"name": "Soil Testing Kit", "category": "Soil", "price": 900,
     "url": "/equipment",
     "keywords": ["soil test", "soil testing", "soil kit"]},

    {"name": "Soil pH Meter", "category": "Soil", "price": 700,
     "url": "/equipment",
     "keywords": ["ph meter", "soil ph", "soil meter"]},

    {"name": "Compost Bin", "category": "Soil", "price": 850,
     "url": "/equipment",
     "keywords": ["compost bin", "composting"]}

]


# =========================================================
# FARMING INFORMATION
# =========================================================

FARMING_INFO = {

    "seeds": "Choose seeds according to crop, season, soil and local growing conditions.",

    "soil": "Soil preparation includes loosening the soil, removing weeds and maintaining suitable soil conditions.",

    "fertilizer": "Fertilizer selection should depend on crop needs, soil condition and recommended agricultural practices.",

    "irrigation": "Irrigation supplies water to crops. Drip, sprinkler and other methods can be selected according to field conditions.",

    "crop care": "Crop care includes watering, nutrition, weed management and monitoring crops for pests and diseases.",

    "tools": "Farm tools are used for digging, planting, weeding, pruning, harvesting and general farm work.",

    "harvesting": "Harvesting tools should be selected according to the crop and harvesting method.",

    "storage": "Proper storage helps protect harvested crops and seeds from moisture and damage."
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

        # -----------------------------------------------
        # Direct product / keyword matching
        # -----------------------------------------------

        for product in PRODUCTS:

            text = (
                product["name"].lower()
                + " "
                + product["category"].lower()
                + " "
                + " ".join(product["keywords"]).lower()
            )

            if query in text:

                if product not in results:
                    results.append(product)


        # -----------------------------------------------
        # Natural farmer requests
        # -----------------------------------------------

        request_groups = {

            "digging": [
                "dig",
                "digging",
                "dig soil",
                "dig ground",
                "digging tool",
                "soil digging",
                "gaddapara",
                "గడ్డపార",
                "గడ్డ పార",
                "खुदाई"
            ],

            "watering": [
                "water",
                "watering",
                "water field",
                "irrigation",
                "నీరు",
                "నీటి",
                "పారుదల",
                "पानी",
                "सिंचाई"
            ],

            "planting": [
                "plant",
                "planting",
                "sowing",
                "seed planting",
                "విత్తడం",
                "నాటడం",
                "बुवाई",
                "पेरणी"
            ],

            "cutting": [
                "cut",
                "cutting",
                "prune",
                "pruning",
                "branch",
                "trim",
                "కొమ్మ",
                "కత్తిర",
                "छाटणी"
            ],

            "seeds": [
                "seed",
                "seeds",
                "విత్తనం",
                "విత్తనాలు",
                "बीज",
                "விதை",
                "ಬೀಜ"
            ],

            "fertilizer": [
                "fertilizer",
                "fertilizers",
                "urea",
                "manure",
                "ఎరువు",
                "ఎరువులు",
                "యూరియా",
                "खाद",
                "उर्वरक"
            ],

            "cropcare": [
                "crop care",
                "crop growth",
                "plant growth",
                "plant care",
                "పంట సంరక్షణ",
                "పంట పెరుగుదల",
                "फसल देखभाल"
            ]
        }


        matched_groups = []

        for group, words in request_groups.items():

            for word in words:

                if word in query:

                    matched_groups.append(group)
                    break


        # -----------------------------------------------
        # Digging
        # -----------------------------------------------

        if "digging" in matched_groups:

            for product in PRODUCTS:

                if product["category"] in [
                    "Tools",
                    "Machinery"
                ]:

                    text = (
                        product["name"].lower()
                        + " "
                        + " ".join(product["keywords"]).lower()
                    )

                    if any(word in text for word in [
                        "gaddapara",
                        "dig",
                        "digging",
                        "hoe",
                        "spade",
                        "shovel",
                        "pickaxe",
                        "cultivator"
                    ]):

                        if product not in results:
                            results.append(product)


        # -----------------------------------------------
        # Watering
        # -----------------------------------------------

        if "watering" in matched_groups:

            for product in PRODUCTS:

                if product["category"] == "Irrigation":

                    if product not in results:
                        results.append(product)


        # -----------------------------------------------
        # Planting
        # -----------------------------------------------

        if "planting" in matched_groups:

            for product in PRODUCTS:

                if product["category"] == "Seeds" or "Seed Drill" in product["name"]:

                    if product not in results:
                        results.append(product)


        # -----------------------------------------------
        # Cutting
        # -----------------------------------------------

        if "cutting" in matched_groups:

            for product in PRODUCTS:

                text = (
                    product["name"].lower()
                    + " "
                    + " ".join(product["keywords"]).lower()
                )

                if any(word in text for word in [
                    "pruning",
                    "cut",
                    "sickle",
                    "axe",
                    "brush cutter"
                ]):

                    if product not in results:
                        results.append(product)


        # -----------------------------------------------
        # Seeds
        # -----------------------------------------------

        if "seeds" in matched_groups:

            for product in PRODUCTS:

                if product["category"] == "Seeds":

                    if product not in results:
                        results.append(product)


        # -----------------------------------------------
        # Fertilizers
        # -----------------------------------------------

        if "fertilizer" in matched_groups:

            for product in PRODUCTS:

                if product["category"] == "Fertilizer":

                    if product not in results:
                        results.append(product)


        # -----------------------------------------------
        # Crop Care
        # -----------------------------------------------

        if "cropcare" in matched_groups:

            for product in PRODUCTS:

                if product["category"] == "Crop Care":

                    if product not in results:
                        results.append(product)


    return render_template(
        "search.html",
        query=query,
        results=results
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
# ADD TO CART
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


# =========================================================
# INCREASE
# =========================================================

@app.route("/increase/<int:index>")
def increase(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):

        cart_items[index]["quantity"] += 1

    session["cart"] = cart_items

    return redirect("/cart")


# =========================================================
# DECREASE
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

    return redirect("/cart")


# =========================================================
# REMOVE
# =========================================================

@app.route("/remove-from-cart/<int:index>")
def remove_from_cart(index):

    cart_items = session.get("cart", [])

    if 0 <= index < len(cart_items):

        cart_items.pop(index)

    session["cart"] = cart_items

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

    name = request.form.get("name", "")
    mobile = request.form.get("mobile", "")
    address = request.form.get("address", "")

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

    return render_template(
        "Delivery.html"
    )


# =========================================================
# RUN
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