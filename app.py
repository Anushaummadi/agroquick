from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "agroquick123"


# =========================================================
# LARGE FARMING PRODUCT CATALOGUE
# =========================================================

PRODUCTS = [

    # =========================
    # FARM TOOLS
    # =========================

    {
        "id": "gaddapara",
        "name": "Gaddapara",
        "category": "Tools",
        "price": 450,
        "image": "/static/images/gaddapara.jpg",
        "description": "Traditional heavy-duty agricultural digging and soil-working tool.",
        "uses": "Used for digging hard soil, breaking compact soil and preparing land.",
        "specifications": "Heavy-duty agricultural hand tool.",
        "stock": "In Stock",
        "keywords": ["gaddapara", "gaddapara tool", "digging tool", "గడ్డపార", "गडापारा"]
    },

    {
        "id": "spade",
        "name": "Agricultural Spade",
        "category": "Tools",
        "price": 550,
        "image": "/static/images/spade.jpg",
        "description": "Strong agricultural spade suitable for digging and turning soil.",
        "uses": "Digging, soil preparation, transplanting and garden work.",
        "specifications": "Metal agricultural spade with strong handle.",
        "stock": "In Stock",
        "keywords": ["spade", "agricultural spade", "digging spade", "పార", "फावड़ा"]
    },

    {
        "id": "shovel",
        "name": "Agricultural Shovel",
        "category": "Tools",
        "price": 500,
        "image": "/static/images/shovel.jpg",
        "description": "Agricultural shovel designed for moving soil, compost and other farm materials.",
        "uses": "Moving soil, manure, compost and loose materials.",
        "specifications": "Durable metal shovel.",
        "stock": "In Stock",
        "keywords": ["shovel", "soil shovel", "farm shovel", "పార", "फावड़ा"]
    },

    {
        "id": "sickle",
        "name": "Agricultural Sickle",
        "category": "Tools",
        "price": 300,
        "image": "/static/images/sickle.jpg",
        "description": "Traditional agricultural cutting tool for harvesting and vegetation management.",
        "uses": "Harvesting crops and cutting grass and vegetation.",
        "specifications": "Curved agricultural cutting blade.",
        "stock": "In Stock",
        "keywords": ["sickle", "harvesting sickle", "crop cutting", "కొడవలి", "दरांती"]
    },

    {
        "id": "hoe",
        "name": "Hand Hoe",
        "category": "Tools",
        "price": 400,
        "image": "/static/images/hoe.jpg",
        "description": "Hand hoe for soil preparation and removal of weeds.",
        "uses": "Loosening soil, weeding and preparing planting areas.",
        "specifications": "Agricultural hand hoe.",
        "stock": "In Stock",
        "keywords": ["hoe", "hand hoe", "weeding hoe", "గొడ్డలి", "कुदाल"]
    },

    {
        "id": "pickaxe",
        "name": "Agricultural Pickaxe",
        "category": "Tools",
        "price": 650,
        "image": "/static/images/pickaxe.jpg",
        "description": "Heavy-duty pickaxe for breaking hard soil and preparing land.",
        "uses": "Breaking hard soil and digging compact ground.",
        "specifications": "Heavy agricultural pickaxe.",
        "stock": "In Stock",
        "keywords": ["pickaxe", "pick axe", "digging", "గొడ్డలి", "कुदाल"]
    },

    {
        "id": "rake",
        "name": "Agricultural Rake",
        "category": "Tools",
        "price": 450,
        "image": "/static/images/rake.jpg",
        "description": "Farm rake for collecting leaves, crop residue and leveling soil.",
        "uses": "Soil leveling, collecting leaves and cleaning farm areas.",
        "specifications": "Agricultural metal rake.",
        "stock": "In Stock",
        "keywords": ["rake", "farm rake", "soil rake", "రేక్"]
    },

    {
        "id": "pruning-shears",
        "name": "Pruning Shears",
        "category": "Tools",
        "price": 350,
        "image": "/static/images/pruning-shears.jpg",
        "description": "Hand pruning tool for cutting small branches and plant growth.",
        "uses": "Pruning plants, branches and garden crops.",
        "specifications": "Hand-operated pruning shears.",
        "stock": "In Stock",
        "keywords": ["pruning shears", "secateur", "pruner", "branch cutter"]
    },

    {
        "id": "hand-weeder",
        "name": "Hand Weeder",
        "category": "Tools",
        "price": 250,
        "image": "/static/images/hand-weeder.jpg",
        "description": "Hand tool designed for removing weeds around crops.",
        "uses": "Manual weed removal and soil loosening.",
        "specifications": "Compact agricultural hand weeder.",
        "stock": "In Stock",
        "keywords": ["weeder", "hand weeder", "weed remover", "కలుపు"]
    },


    # =========================
    # SEEDS
    # =========================

    {
        "id": "rice-seeds",
        "name": "Rice Seeds",
        "category": "Seeds",
        "price": 100,
        "image": "/static/images/rice-seeds.jpg",
        "description": "Quality rice seed suitable for agricultural cultivation.",
        "uses": "Rice and paddy cultivation.",
        "specifications": "Seed suitable for agricultural sowing.",
        "stock": "In Stock",
        "keywords": ["rice", "rice seeds", "paddy", "paddy seeds", "వరి", "వరి విత్తనాలు", "धान"]
    },

    {
        "id": "wheat-seeds",
        "name": "Wheat Seeds",
        "category": "Seeds",
        "price": 120,
        "image": "/static/images/wheat-seeds.jpg",
        "description": "Agricultural wheat seeds for crop cultivation.",
        "uses": "Wheat cultivation.",
        "specifications": "Wheat seed for agricultural sowing.",
        "stock": "In Stock",
        "keywords": ["wheat", "wheat seeds", "గోధుమ", "గోధుమ విత్తనాలు", "गेहूं"]
    },

    {
        "id": "maize-seeds",
        "name": "Maize Seeds",
        "category": "Seeds",
        "price": 150,
        "image": "/static/images/maize-seeds.jpg",
        "description": "Maize seed for agricultural crop production.",
        "uses": "Maize and corn cultivation.",
        "specifications": "Maize seed for sowing.",
        "stock": "In Stock",
        "keywords": ["maize", "corn", "maize seeds", "మొక్కజొన్న", "मक्का"]
    },

    {
        "id": "cotton-seeds",
        "name": "Cotton Seeds",
        "category": "Seeds",
        "price": 650,
        "image": "/static/images/cotton-seeds.jpg",
        "description": "Cotton seed for agricultural cultivation.",
        "uses": "Cotton farming.",
        "specifications": "Agricultural cotton seed.",
        "stock": "In Stock",
        "keywords": ["cotton", "cotton seeds", "పత్తి", "पत्ता"]
    },

    {
        "id": "groundnut-seeds",
        "name": "Groundnut Seeds",
        "category": "Seeds",
        "price": 180,
        "image": "/static/images/groundnut-seeds.jpg",
        "description": "Groundnut seed suitable for crop cultivation.",
        "uses": "Groundnut farming.",
        "specifications": "Agricultural groundnut seed.",
        "stock": "In Stock",
        "keywords": ["groundnut", "peanut", "groundnut seeds", "వేరుశెనగ"]
    },

    {
        "id": "chilli-seeds",
        "name": "Chilli Seeds",
        "category": "Seeds",
        "price": 220,
        "image": "/static/images/chilli-seeds.jpg",
        "description": "Chilli seeds for agricultural and vegetable cultivation.",
        "uses": "Chilli cultivation.",
        "specifications": "Vegetable crop seed.",
        "stock": "In Stock",
        "keywords": ["chilli", "chili", "chilli seeds", "మిరప", "మిరప విత్తనాలు"]
    },

    {
        "id": "tomato-seeds",
        "name": "Tomato Seeds",
        "category": "Seeds",
        "price": 180,
        "image": "/static/images/tomato-seeds.jpg",
        "description": "Tomato seeds suitable for vegetable cultivation.",
        "uses": "Tomato farming.",
        "specifications": "Vegetable crop seed.",
        "stock": "In Stock",
        "keywords": ["tomato", "tomato seeds", "టమాటా", "टमाटर"]
    },

    {
        "id": "vegetable-seeds",
        "name": "Vegetable Seeds",
        "category": "Seeds",
        "price": 80,
        "image": "/static/images/vegetable-seeds.jpg",
        "description": "Vegetable seed collection for home gardens and farming.",
        "uses": "Vegetable cultivation.",
        "specifications": "Mixed vegetable seed category.",
        "stock": "In Stock",
        "keywords": ["vegetable", "vegetables", "vegetable seeds", "కూరగాయలు"]
    },


    # =========================
    # FERTILIZERS
    # =========================

    {
        "id": "urea",
        "name": "Urea Fertilizer",
        "category": "Fertilizer",
        "price": 500,
        "image": "/static/images/urea.jpg",
        "description": "Nitrogen fertilizer used as a nutrient source in crop production.",
        "uses": "Nitrogen nutrition for crops.",
        "specifications": "Agricultural fertilizer product.",
        "stock": "In Stock",
        "keywords": ["urea", "urea fertilizer", "యూరియా", "यूरिया"]
    },

    {
        "id": "dap",
        "name": "DAP Fertilizer",
        "category": "Fertilizer",
        "price": 1350,
        "image": "/static/images/dap.jpg",
        "description": "Di-ammonium phosphate fertilizer used as a source of nitrogen and phosphorus.",
        "uses": "Crop nutrient management.",
        "specifications": "DAP fertilizer.",
        "stock": "In Stock",
        "keywords": ["dap", "dap fertilizer", "di ammonium phosphate", "డిఎపి"]
    },

    {
        "id": "npk",
        "name": "NPK Fertilizer",
        "category": "Fertilizer",
        "price": 900,
        "image": "/static/images/npk.jpg",
        "description": "Compound fertilizer providing nitrogen, phosphorus and potassium nutrients.",
        "uses": "Crop nutrient management.",
        "specifications": "NPK compound fertilizer.",
        "stock": "In Stock",
        "keywords": ["npk", "npk fertilizer", "ఎన్ పి కె"]
    },

    {
        "id": "potash",
        "name": "Potash Fertilizer",
        "category": "Fertilizer",
        "price": 800,
        "image": "/static/images/potash.jpg",
        "description": "Potassium fertilizer used in crop nutrient management.",
        "uses": "Potassium nutrition for crops.",
        "specifications": "Agricultural potash fertilizer.",
        "stock": "In Stock",
        "keywords": ["potash", "potassium fertilizer", "పొటాష్"]
    },

    {
        "id": "vermicompost",
        "name": "Vermicompost",
        "category": "Organic Farming",
        "price": 300,
        "image": "/static/images/vermicompost.jpg",
        "description": "Organic manure produced through earthworm-based composting.",
        "uses": "Organic soil improvement and nutrient management.",
        "specifications": "Organic manure.",
        "stock": "In Stock",
        "keywords": ["vermicompost", "organic manure", "compost", "వర్మీకంపోస్ట్"]
    },


    # =========================
    # IRRIGATION
    # =========================

    {
        "id": "water-pump",
        "name": "Water Pump",
        "category": "Irrigation",
        "price": 2500,
        "image": "/static/images/water-pump.jpg",
        "description": "Agricultural water pump for irrigation and water transfer.",
        "uses": "Farm irrigation and water transfer.",
        "specifications": "Agricultural irrigation equipment.",
        "stock": "In Stock",
        "keywords": ["water pump", "pump", "irrigation pump", "నీటి పంపు", "मोटर"]
    },

    {
        "id": "drip-irrigation-kit",
        "name": "Drip Irrigation Kit",
        "category": "Irrigation",
        "price": 1800,
        "image": "/static/images/drip-kit.jpg",
        "description": "Drip irrigation components for controlled water delivery to crops.",
        "uses": "Efficient crop irrigation.",
        "specifications": "Drip irrigation kit.",
        "stock": "In Stock",
        "keywords": ["drip", "drip irrigation", "drip kit", "డ్రిప్"]
    },

    {
        "id": "sprinkler-set",
        "name": "Agricultural Sprinkler Set",
        "category": "Irrigation",
        "price": 1200,
        "image": "/static/images/sprinkler.jpg",
        "description": "Sprinkler irrigation equipment for distributing water over crop areas.",
        "uses": "Farm irrigation.",
        "specifications": "Agricultural sprinkler set.",
        "stock": "In Stock",
        "keywords": ["sprinkler", "sprinkler set", "irrigation sprinkler", "స్ప్రింక్లర్"]
    },

    {
        "id": "irrigation-pipe",
        "name": "Agricultural Irrigation Pipe",
        "category": "Irrigation",
        "price": 700,
        "image": "/static/images/irrigation-pipe.jpg",
        "description": "Pipe suitable for agricultural water transportation.",
        "uses": "Moving irrigation water.",
        "specifications": "Agricultural irrigation pipe.",
        "stock": "In Stock",
        "keywords": ["irrigation pipe", "farm pipe", "water pipe", "నీటి పైపు"]
    },


    # =========================
    # FARM EQUIPMENT
    # =========================

    {
        "id": "seed-drill",
        "name": "Seed Drill",
        "category": "Farm Equipment",
        "price": 8000,
        "image": "/static/images/seed-drill.jpg",
        "description": "Agricultural equipment designed for placing seeds in prepared soil.",
        "uses": "Seed sowing and planting.",
        "specifications": "Agricultural seed drilling equipment.",
        "stock": "In Stock",
        "keywords": ["seed drill", "sowing machine", "planting machine", "విత్తే యంత్రం"]
    },

    {
        "id": "mini-cultivator",
        "name": "Mini Cultivator",
        "category": "Farm Equipment",
        "price": 12000,
        "image": "/static/images/mini-cultivator.jpg",
        "description": "Compact cultivation equipment for soil preparation.",
        "uses": "Soil cultivation and preparation.",
        "specifications": "Compact agricultural cultivator.",
        "stock": "In Stock",
        "keywords": ["cultivator", "mini cultivator", "soil cultivator", "సాగు యంత్రం"]
    },

    {
        "id": "sprayer",
        "name": "Agricultural Sprayer",
        "category": "Farm Equipment",
        "price": 3500,
        "image": "/static/images/sprayer.jpg",
        "description": "Agricultural sprayer for applying approved crop-care products.",
        "uses": "Crop spraying.",
        "specifications": "Agricultural spraying equipment.",
        "stock": "In Stock",
        "keywords": ["sprayer", "farm sprayer", "crop sprayer", "స్ప్రేయర్"]
    },

    {
        "id": "brush-cutter",
        "name": "Brush Cutter",
        "category": "Farm Equipment",
        "price": 8500,
        "image": "/static/images/brush-cutter.jpg",
        "description": "Powered equipment for cutting grass and unwanted vegetation.",
        "uses": "Vegetation and grass cutting.",
        "specifications": "Agricultural brush-cutting equipment.",
        "stock": "In Stock",
        "keywords": ["brush cutter", "grass cutter", "vegetation cutter"]
    },


    # =========================
    # CROP CARE
    # =========================

    {
        "id": "micronutrient-mix",
        "name": "Micronutrient Mix",
        "category": "Crop Care",
        "price": 400,
        "image": "/static/images/micronutrient.jpg",
        "description": "Micronutrient product used as part of crop nutrient management.",
        "uses": "Crop micronutrient management.",
        "specifications": "Agricultural micronutrient product.",
        "stock": "In Stock",
        "keywords": ["micronutrient", "micro nutrient", "crop nutrition", "సూక్ష్మ పోషకాలు"]
    },

    {
        "id": "plant-growth-support",
        "name": "Plant Growth Support",
        "category": "Crop Care",
        "price": 250,
        "image": "/static/images/plant-growth.jpg",
        "description": "Crop-care product intended to support plant growth when used according to its label.",
        "uses": "Plant and crop-care management.",
        "specifications": "Agricultural crop-care product.",
        "stock": "In Stock",
        "keywords": ["plant growth", "growth support", "crop care", "పంట సంరక్షణ"]
    },

    {
        "id": "neem-crop-care",
        "name": "Neem Based Crop Care",
        "category": "Crop Care",
        "price": 300,
        "image": "/static/images/neem.jpg",
        "description": "Neem-based agricultural crop-care product.",
        "uses": "Crop-care management according to product directions.",
        "specifications": "Neem-based agricultural product.",
        "stock": "In Stock",
        "keywords": ["neem", "neem crop care", "organic crop care", "వేప"]
    },


    # =========================
    # NURSERY & GARDEN
    # =========================

    {
        "id": "seed-tray",
        "name": "Seedling Nursery Tray",
        "category": "Nursery",
        "price": 120,
        "image": "/static/images/seed-tray.jpg",
        "description": "Reusable tray for raising seedlings.",
        "uses": "Nursery and seedling production.",
        "specifications": "Multi-cell nursery tray.",
        "stock": "In Stock",
        "keywords": ["seed tray", "nursery tray", "seedling tray", "నర్సరీ ట్రే"]
    },

    {
        "id": "grow-bag",
        "name": "Plant Grow Bag",
        "category": "Nursery",
        "price": 100,
        "image": "/static/images/grow-bag.jpg",
        "description": "Grow bag suitable for container-based crop and plant cultivation.",
        "uses": "Vegetable, nursery and home farming.",
        "specifications": "Reusable plant grow bag.",
        "stock": "In Stock",
        "keywords": ["grow bag", "plant bag", "nursery bag", "గ్రో బ్యాగ్"]
    },

    {
        "id": "plant-support",
        "name": "Plant Support Sticks",
        "category": "Nursery",
        "price": 150,
        "image": "/static/images/plant-support.jpg",
        "description": "Supports for plants that need physical growth support.",
        "uses": "Supporting vegetable and garden plants.",
        "specifications": "Agricultural plant-support accessories.",
        "stock": "In Stock",
        "keywords": ["plant support", "support sticks", "plant stake"]
    },


    # =========================
    # HARVEST & STORAGE
    # =========================

    {
        "id": "harvest-knife",
        "name": "Harvesting Knife",
        "category": "Harvesting",
        "price": 280,
        "image": "/static/images/harvest-knife.jpg",
        "description": "Agricultural hand tool used for harvesting and cutting suitable crops.",
        "uses": "Harvesting and crop cutting.",
        "specifications": "Agricultural harvesting hand tool.",
        "stock": "In Stock",
        "keywords": ["harvesting knife", "harvest knife", "crop knife"]
    },

    {
        "id": "farm-crate",
        "name": "Agricultural Plastic Crate",
        "category": "Storage",
        "price": 450,
        "image": "/static/images/farm-crate.jpg",
        "description": "Reusable crate for handling and transporting agricultural produce.",
        "uses": "Produce handling and transportation.",
        "specifications": "Reusable agricultural crate.",
        "stock": "In Stock",
        "keywords": ["farm crate", "plastic crate", "vegetable crate", "క్రేట్"]
    },

    {
        "id": "tarpaulin",
        "name": "Agricultural Tarpaulin",
        "category": "Storage",
        "price": 900,
        "image": "/static/images/tarpaulin.jpg",
        "description": "Protective agricultural sheet used for covering and handling farm materials.",
        "uses": "Crop covering, drying and material protection.",
        "specifications": "Agricultural tarpaulin sheet.",
        "stock": "In Stock",
        "keywords": ["tarpaulin", "farm sheet", "crop cover", "టార్పాలిన్"]
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

    query = request.args.get("query", "").strip().lower()

    if query:

        results = []

        for product in PRODUCTS:

            searchable_text = " ".join(
                [
                    product["name"],
                    product["category"],
                    " ".join(product["keywords"])
                ]
            ).lower()

            if query in searchable_text:
                results.append(product)

    else:
        results = []

    return render_template(
        "search.html",
        query=query,
        results=results
    )


# =========================================================
# INDIVIDUAL PRODUCT PAGE
# =========================================================

@app.route("/product/<product_id>")
def product_detail(product_id):

    product = next(
        (
            product
            for product in PRODUCTS
            if product["id"] == product_id
        ),
        None
    )

    if product is None:
        return "Product not found", 404

    return render_template(
        "product.html",
        product=product
    )


# =========================================================
# CATEGORY PAGES
# =========================================================

@app.route("/seeds")
def seeds():

    products = [
        product for product in PRODUCTS
        if product["category"] == "Seeds"
    ]

    return render_template(
        "seeds.html",
        products=products
    )


@app.route("/fertilizer")
def fertilizer():

    products = [
        product for product in PRODUCTS
        if product["category"] == "Fertilizer"
    ]

    return render_template(
        "Fertilizer.html",
        products=products
    )


@app.route("/equipment")
def equipment():

    products = [
        product for product in PRODUCTS
        if product["category"] == "Farm Equipment"
    ]

    return render_template(
        "equipment.html",
        products=products
    )


@app.route("/tools")
def tools():

    products = [
        product for product in PRODUCTS
        if product["category"] == "Tools"
    ]

    return render_template(
        "tools.html",
        products=products
    )


@app.route("/crop-care")
def crop_care():

    products = [
        product for product in PRODUCTS
        if product["category"] == "Crop Care"
    ]

    return render_template(
        "crop_care.html",
        products=products
    )


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

        cart_items.append(
            {
                "product": product,
                "price": price,
                "quantity": 1
            }
        )

    session["cart"] = cart_items

    return redirect("/cart")


# =========================================================
# INCREASE
# =========================================================

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


# =========================================================
# DECREASE
# =========================================================

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


# =========================================================
# REMOVE
# =========================================================

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


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout")
def checkout():

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
# START APPLICATION
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