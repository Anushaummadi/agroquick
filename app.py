from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "agroquick123"


# =========================================================
# PRODUCT CATALOG
# =========================================================

PRODUCTS = [

    # SEEDS
    {
        "name": "Rice Seeds",
        "category": "Seeds",
        "price": 100,
        "url": "/seeds",
        "keywords": [
            "rice", "seed", "seeds", "paddy",
            "వరి", "వరి విత్తనాలు",
            "బియ్యం", "बीज", "धान", "तांदूळ"
        ]
    },

    {
        "name": "Wheat Seeds",
        "category": "Seeds",
        "price": 120,
        "url": "/seeds",
        "keywords": [
            "wheat", "seed", "seeds",
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
            "maize", "corn", "seed", "seeds",
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
            "vegetable", "vegetables",
            "seed", "seeds",
            "కూరగాయలు", "కూరగాయల విత్తనాలు",
            "सब्जी", "भाजी", "காய்கறி", "ತರಕಾರಿ"
        ]
    },


    # FERTILIZER
    {
        "name": "Urea Fertilizer",
        "category": "Fertilizer",
        "price": 500,
        "url": "/fertilizer",
        "keywords": [
            "urea",
            "యూరియా",
            "यूरिया",
            "युरिया",
            "யூரியா",
            "ಯೂರಿಯಾ"
        ]
    },

    {
        "name": "Fertilizer",
        "category": "Fertilizer",
        "price": 450,
        "url": "/fertilizer",
        "keywords": [
            "fertilizer", "fertilizers", "manure",
            "ఎరువు", "ఎరువులు",
            "खाद", "उर्वरक", "खत",
            "உரம்", "ರಸಗೊಬ್ಬರ"
        ]
    },


    # EQUIPMENT
    {
        "name": "Water Pump",
        "category": "Equipment",
        "price": 2500,
        "url": "/equipment",
        "keywords": [
            "water pump", "pump", "watering",
            "water", "irrigation",
            "నీటి పంపు", "నీటి మోటార్",
            "పారుదల",
            "पानी का पंप", "सिंचाई",
            "पाण्याचा पंप",
            "தண்ணீர் பம்ப்",
            "நீர்ப்பாசனம்",
            "ನೀರಿನ ಪಂಪ್"
        ]
    },

    {
        "name": "Seed Drill",
        "category": "Equipment",
        "price": 8000,
        "url": "/equipment",
        "keywords": [
            "seed drill", "planting", "sowing",
            "seed planting", "seeds planting",
            "విత్తడం", "విత్తనాలు వేయడం",
            "बुवाई", "बीज बोना",
            "पेरणी",
            "விதைப்பு",
            "ಬಿತ್ತನೆ"
        ]
    },

    {
        "name": "Mini Cultivator",
        "category": "Equipment",
        "price": 12000,
        "url": "/equipment",
        "keywords": [
            "cultivator", "cultivation",
            "soil cultivation", "soil",
            "plough", "plowing",
            "నేల", "నేల సాగు",
            "मिट्टी", "जुताई",
            "माती", "नांगरणी",
            "மண்", "உழவு",
            "ಮಣ್ಣು", "ಉಳುಮೆ"
        ]
    },

    {
        "name": "Sprayer",
        "category": "Equipment",
        "price": 3500,
        "url": "/equipment",
        "keywords": [
            "sprayer", "spraying", "spray",
            "crop spraying", "pesticide spraying",
            "స్ప్రేయర్", "పిచికారీ",
            "स्प्रे", "छिड़काव",
            "फवारणी",
            "தெளிப்பான்",
            "ಸಿಂಪಡಣೆ"
        ]
    },


    # TOOLS
    {
        "name": "Hand Hoe",
        "category": "Tools",
        "price": 450,
        "url": "/tools",
        "keywords": [
            "hoe", "hand hoe", "dig", "digging",
            "soil preparation", "soil",
            "మట్టి తవ్వడం", "మట్టి",
            "खुदाई", "मिट्टी",
            "खोदणे",
            "தோண்டுதல்",
            "ಮಣ್ಣು ಅಗೆಯುವುದು"
        ]
    },

    {
        "name": "Pruning Shears",
        "category": "Tools",
        "price": 350,
        "url": "/tools",
        "keywords": [
            "pruning", "pruning shears",
            "cut branches", "cutting branches",
            "trim plants", "cut plants",
            "కొమ్మలు కత్తిరించడం",
            "पौधे काटना", "शाखाएं काटना",
            "फांद्या कापणे",
            "கிளைகளை வெட்ட",
            "ಕೊಂಬೆಗಳನ್ನು ಕತ್ತರಿಸುವುದು"
        ]
    },

    {
        "name": "Watering Can",
        "category": "Tools",
        "price": 250,
        "url": "/tools",
        "keywords": [
            "watering can", "watering plants",
            "water plants", "plants water",
            "మొక్కలకు నీరు",
            "पौधों को पानी",
            "झाडांना पाणी",
            "தாவரங்களுக்கு தண்ணீர்",
            "ಸಸ್ಯಗಳಿಗೆ ನೀರು"
        ]
    },

    {
        "name": "Hand Cultivator",
        "category": "Tools",
        "price": 300,
        "url": "/tools",
        "keywords": [
            "hand cultivator", "loosen soil",
            "loosening soil", "soil tool",
            "నేలను వదులుగా చేయడం",
            "मिट्टी ढीली करना",
            "माती सैल करणे",
            "மண்ணை தளர்த்த",
            "ಮಣ್ಣು ಸಡಿಲಗೊಳಿಸುವುದು"
        ]
    },


    # CROP CARE
    {
        "name": "Plant Growth Support",
        "category": "Crop Care",
        "price": 250,
        "url": "/crop-care",
        "keywords": [
            "plant growth", "crop growth",
            "growth support", "healthy growth",
            "పంట పెరుగుదల", "మొక్కల పెరుగుదల",
            "फसल की वृद्धि", "पौधों की वृद्धि",
            "पीक वाढ",
            "பயிர் வளர்ச்சி",
            "ಬೆಳೆ ಬೆಳವಣಿಗೆ"
        ]
    },

    {
        "name": "Neem Based Crop Care",
        "category": "Crop Care",
        "price": 300,
        "url": "/crop-care",
        "keywords": [
            "neem", "neem crop care",
            "plant care", "crop protection",
            "వేప", "పంట సంరక్షణ",
            "नीम", "फसल सुरक्षा",
            "कडुनिंब",
            "வேம்பு",
            "ಬೇವು"
        ]
    },

    {
        "name": "Micronutrient Mix",
        "category": "Crop Care",
        "price": 400,
        "url": "/crop-care",
        "keywords": [
            "micronutrient", "nutrients",
            "plant nutrients", "crop nutrients",
            "పోషకాలు", "సూక్ష్మ పోషకాలు",
            "सूक्ष्म पोषक",
            "पोषक तत्व",
            "सूक्ष्म अन्नद्रव्ये",
            "ஊட்டச்சத்துக்கள்",
            "ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶಗಳು"
        ]
    },

    {
        "name": "Crop Growth Booster",
        "category": "Crop Care",
        "price": 350,
        "url": "/crop-care",
        "keywords": [
            "growth booster", "crop booster",
            "plant booster", "crop growth",
            "పంట పెరుగుదల", "గ్రోత్ బూస్టర్",
            "फसल बूस्टर",
            "पीक वाढ",
            "பயிர் வளர்ச்சி",
            "ಬೆಳೆ ಬೆಳವಣಿಗೆ"
        ]
    }
]


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

    original_query = request.args.get(
        "query",
        ""
    ).strip()

    query = original_query.lower()

    results = []


    if query:

        # -------------------------------------------------
        # 1. DIRECT PRODUCT / KEYWORD MATCH
        # -------------------------------------------------

        for product in PRODUCTS:

            product_text = (
                product["name"].lower()
                + " "
                + product["category"].lower()
            )

            matched = False

            if query in product_text:
                matched = True

            else:

                for keyword in product["keywords"]:

                    if keyword.lower() in query:
                        matched = True
                        break

            if matched and product not in results:
                results.append(product)


        # -------------------------------------------------
        # 2. FARMING INTENT MATCHING
        # -------------------------------------------------

        intent_rules = {

            "seeds": [
                "seed",
                "seeds",
                "planting",
                "sowing",
                "want to plant",
                "need seed",
                "need seeds",
                "విత్తనం",
                "విత్తనాలు",
                "విత్తడం",
                "बीज",
                "बुवाई",
                "बियाणे",
                "விதைகள்",
                "விதைப்பு",
                "ಬೀಜಗಳು",
                "ಬಿತ್ತನೆ"
            ],

            "fertilizer": [
                "fertilizer",
                "fertilizers",
                "manure",
                "plant food",
                "crop nutrients",
                "need fertilizer",
                "ఎరువు",
                "ఎరువులు",
                "खाद",
                "उर्वरक",
                "खत",
                "உரம்",
                "ರಸಗೊಬ್ಬರ"
            ],

            "equipment": [
                "equipment",
                "machine",
                "machines",
                "farming machine",
                "farm machine",
                "agriculture machine",
                "farming equipment",
                "agricultural equipment",
                "వ్యవసాయ యంత్రం",
                "వ్యవసాయ పరికరాలు",
                "कृषि उपकरण",
                "शेती उपकरणे",
                "விவசாய உபகரணங்கள்",
                "ಕೃಷಿ ಉಪಕರಣಗಳು"
            ],

            "tools": [
                "tool",
                "tools",
                "farming tool",
                "farming tools",
                "hand tool",
                "farm tools",
                "వ్యవసాయ పనిముట్లు",
                "పనిముట్లు",
                "कृषि उपकरण",
                "शेतीची साधने",
                "விவசாய கருவிகள்",
                "ಕೃಷಿ ಉಪಕರಣಗಳು"
            ],

            "crop care": [
                "crop care",
                "plant care",
                "crop protection",
                "plant protection",
                "crop growth",
                "plant growth",
                "healthy crop",
                "healthy plant",
                "pest",
                "pests",
                "crop problem",
                "plant problem",
                "పంట సంరక్షణ",
                "మొక్కల సంరక్షణ",
                "పంట పెరుగుదల",
                "फसल देखभाल",
                "फसल सुरक्षा",
                "पीक संरक्षण",
                "பயிர் பராமரிப்பு",
                "ಬೆಳೆ ಆರೈಕೆ"
            ]
        }


        # -------------------------------------------------
        # 3. SPECIFIC FARMING REQUESTS
        # -------------------------------------------------

        specific_requests = {

            "watering": [
                "water my farm",
                "water my field",
                "watering",
                "water plants",
                "water crops",
                "irrigation",
                "need water",
                "need irrigation",
                "నీరు పెట్టాలి",
                "పంటకు నీరు",
                "పొలానికి నీరు",
                "सिंचाई",
                "पानी देना",
                "शेताला पाणी",
                "தண்ணீர்",
                "நீர்ப்பாசனம்",
                "ನೀರಾವರಿ"
            ],

            "spraying": [
                "spray",
                "spraying",
                "sprayer",
                "spray crops",
                "spray plants",
                "pesticide spray",
                "crop spraying",
                "పిచికారీ",
                "స్ప్రే",
                "పంటకు స్ప్రే",
                "स्प्रे",
                "छिड़काव",
                "फवारणी",
                "தெளிப்பு",
                "ಸಿಂಪಡಣೆ"
            ],

            "cutting": [
                "cut branches",
                "cut branch",
                "cut plants",
                "trim plants",
                "pruning",
                "prune",
                "branches",
                "కొమ్మలు కత్తిరించాలి",
                "కొమ్మలు కత్తిరించడం",
                "शाखाएं काटना",
                "पौधे काटना",
                "फांद्या कापणे",
                "கிளைகளை வெட்ட",
                "ಕೊಂಬೆಗಳನ್ನು ಕತ್ತರಿಸುವುದು"
            ],

            "soil": [
                "dig soil",
                "digging soil",
                "soil preparation",
                "loosen soil",
                "prepare soil",
                "cultivation",
                "cultivate soil",
                "మట్టి తవ్వాలి",
                "నేల సిద్ధం",
                "మట్టి వదులుగా",
                "मिट्टी तैयार",
                "जुताई",
                "माती तयार",
                "மண் தயாரிப்பு",
                "மண்ணை தளர்த்த",
                "ಮಣ್ಣು ತಯಾರಿಕೆ"
            ],

            "plant_growth": [
                "plant growth",
                "crop growth",
                "help my plants grow",
                "help crops grow",
                "healthy growth",
                "growth booster",
                "పంట పెరగాలి",
                "మొక్క పెరుగుదల",
                "फसल बढ़ाना",
                "पौधे की वृद्धि",
                "पीक वाढ",
                "பயிர் வளர்ச்சி",
                "ಬೆಳೆ ಬೆಳವಣಿಗೆ"
            ]
        }


        # -------------------------------------------------
        # 4. ADD CATEGORY RESULTS
        # -------------------------------------------------

        for category, words in intent_rules.items():

            for word in words:

                if word in query:

                    for product in PRODUCTS:

                        if (
                            product["category"].lower()
                            == category
                        ):
                            if product not in results:
                                results.append(product)

                    break


        # -------------------------------------------------
        # 5. ADD SPECIFIC PRODUCT RESULTS
        # -------------------------------------------------

        if any(word in query for word in specific_requests["watering"]):

            for product in PRODUCTS:

                if product["name"] in [
                    "Water Pump",
                    "Watering Can"
                ]:
                    if product not in results:
                        results.append(product)


        if any(word in query for word in specific_requests["spraying"]):

            for product in PRODUCTS:

                if product["name"] in [
                    "Sprayer",
                    "Neem Based Crop Care"
                ]:
                    if product not in results:
                        results.append(product)


        if any(word in query for word in specific_requests["cutting"]):

            for product in PRODUCTS:

                if product["name"] == "Pruning Shears":

                    if product not in results:
                        results.append(product)


        if any(word in query for word in specific_requests["soil"]):

            for product in PRODUCTS:

                if product["name"] in [
                    "Hand Hoe",
                    "Hand Cultivator",
                    "Mini Cultivator"
                ]:
                    if product not in results:
                        results.append(product)


        if any(word in query for word in specific_requests["plant_growth"]):

            for product in PRODUCTS:

                if product["category"] == "Crop Care":

                    if product not in results:
                        results.append(product)


    return render_template(
        "search.html",
        query=original_query,
        results=results
    )


# =========================================================
# PRODUCT PAGES
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

    retu