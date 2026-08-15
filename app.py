from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify
)
import sqlite3
import os
from datetime import datetime
from functools import wraps

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = BASE_DIR

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATABASE = os.path.join(BASE_DIR, "agroquick.db")

# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = "agroquick123"

# ============================================================
# DATABASE
# ============================================================

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def ensure_column(db, table, column, definition):
    columns = [
        row["name"]
        for row in db.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()
    ]

    if column not in columns:
        db.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )


def init_db():
    db = get_db()

    # USERS
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            address TEXT,
            location TEXT,
            created_at TEXT
        )
    """)

    ensure_column(db, "users", "phone", "TEXT")
    ensure_column(db, "users", "address", "TEXT")
    ensure_column(db, "users", "location", "TEXT")
    ensure_column(db, "users", "created_at", "TEXT")

    # CATEGORIES
    db.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    categories = [
        "Seeds",
        "Fertilizer",
        "Tools",
        "Equipment",
        "Cropcare",
        "Irrigation",
        "Pesticides",
        "Organic Farming",
        "Nursery",
        "Animal Farming"
    ]

    for name in categories:
        db.execute(
            "INSERT OR IGNORE INTO categories(name) VALUES(?)",
            (name,)
        )

    # PRODUCTS
    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            description TEXT,
            stock INTEGER DEFAULT 100,
            delivery_time TEXT DEFAULT '20-30 minutes',
            created_at TEXT
        )
    """)

    ensure_column(db, "products", "stock", "INTEGER DEFAULT 100")
    ensure_column(
        db, "products",
        "delivery_time",
        "TEXT DEFAULT '20-30 minutes'"
    )
    ensure_column(db, "products", "created_at", "TEXT")

    # ========================================================
    # CART ITEMS - PERMANENT CART FOR EACH LOGGED-IN USER
    # ========================================================

    db.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            UNIQUE(user_id, product_id)
        )
    """)

    # ORDERS
    db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer_name TEXT,
            phone TEXT,
            address TEXT,
            total REAL,
            status TEXT,
            delivery_time TEXT,
            created_at TEXT
        )
    """)

    ensure_column(db, "orders", "phone", "TEXT")
    ensure_column(db, "orders", "address", "TEXT")
    ensure_column(db, "orders", "status", "TEXT")
    ensure_column(db, "orders", "delivery_time", "TEXT")
    ensure_column(db, "orders", "created_at", "TEXT")

    # ORDER ITEMS
    db.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            subtotal REAL
        )
    """)

    # ========================================================
    # PRODUCTS
    # ========================================================

    product_count = db.execute(
        "SELECT COUNT(*) AS count FROM products"
    ).fetchone()["count"]

    if product_count == 0:
        product_data = [
            # SEEDS
            ("Tomato Seeds", "Seeds", 99, "tomato-seeds.jpg",
             "Quality tomato seeds for farming."),
            ("Chilli Seeds", "Seeds", 89, "chilli-seeds.jpg",
             "Quality chilli seeds."),
            ("Brinjal Seeds", "Seeds", 79, "brinjal-seeds.jpg",
             "Healthy brinjal seeds."),
            ("Okra Seeds", "Seeds", 85, "okra-seeds.jpg",
             "Quality okra seeds."),
            ("Maize Seeds", "Seeds", 199, "maize-seeds.jpg",
             "High quality maize seeds."),
            ("Paddy Seeds", "Seeds", 299, "paddy.png",
             "Quality paddy seeds."),
            ("Groundnut Seeds", "Seeds", 249, "groundnut-seeds.jpg",
             "Quality groundnut seeds."),
            ("Cotton Seeds", "Seeds", 399, "cotton-seeds.jpg",
             "High quality cotton seeds."),
            ("Sunflower Seeds", "Seeds", 199, "sunflower-seeds.jpg",
             "Quality sunflower seeds."),
            ("Wheat Seeds", "Seeds", 149, "wheat-seeds.jpg",
             "Quality wheat seeds."),

            # FERTILIZER
            ("Urea Fertilizer", "Fertilizer", 299, "urea.jpg",
             "Nitrogen fertilizer for crops."),
            ("DAP Fertilizer", "Fertilizer", 499, "dap.jpg",
             "Nitrogen and phosphorus fertilizer."),
            ("NPK Fertilizer", "Fertilizer", 599, "npk.jpg",
             "Balanced NPK fertilizer."),
            ("Potash Fertilizer", "Fertilizer", 449, "potash.jpg",
             "Potassium fertilizer."),
            ("Organic Fertilizer", "Fertilizer", 499,
             "organic-fertilizer.jpg",
             "Organic fertilizer for healthy crops."),

            # TOOLS
            ("Hand Hoe", "Tools", 299, "hoe.jpg",
             "Strong agricultural hand hoe."),
            ("Garden Spade", "Tools", 399, "spade.jpg",
             "Strong digging spade."),
            ("Hand Cultivator", "Tools", 249, "cultivator.jpg",
             "Soil loosening tool."),
            ("Pruning Cutter", "Tools", 249, "pruner.jpg",
             "Useful pruning cutter."),
            ("Sickle", "Tools", 199, "sickle.jpg",
             "Durable harvesting sickle."),
            ("Weeding Tool", "Tools", 229, "weeder.jpg",
             "Useful tool for removing weeds."),

            # EQUIPMENT
            ("Water Pump", "Equipment", 4999, "water-pump.jpg",
             "Agricultural water pump."),
            ("Agricultural Sprayer", "Equipment", 1299, "sprayer.jpg",
             "Agricultural crop sprayer."),
            ("Knapsack Sprayer", "Equipment", 1899,
             "knapsack-sprayer.jpg",
             "Backpack agricultural sprayer."),

            # IRRIGATION
            ("Drip Irrigation Kit", "Irrigation", 2499, "drip-kit.jpg",
             "Efficient drip irrigation kit."),
            ("Water Pipe", "Irrigation", 799, "water-pipe.jpg",
             "Agricultural water pipe."),
            ("Drip Emitters", "Irrigation", 499, "drip-emitter.jpg",
             "Drip irrigation emitters."),

            # CROPCARE
            ("Crop Care Kit", "Cropcare", 699, "crop-care-kit.jpg",
             "Useful crop care products."),
            ("Plant Growth Booster", "Cropcare", 399,
             "plant-growth-booster.jpg",
             "Plant growth booster."),

            # ORGANIC
            ("Organic Compost", "Organic Farming", 299, "organic-compost.jpg",
             "Organic compost for farming."),

            # NURSERY
            ("Tomato Plant", "Nursery", 49, "tomato-plant.jpg",
             "Healthy tomato plant."),
            ("Mango Sapling", "Nursery", 149, "mango-sapling.jpg",
             "Healthy mango sapling."),
            ("Guava Sapling", "Nursery", 129, "guava-sapling.jpg",
             "Healthy guava sapling.")
        ]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for name, category, price, image, description in product_data:
            category_row = db.execute(
                """
                SELECT id FROM categories
                WHERE LOWER(name)=LOWER(?)
                """,
                (category,)
            ).fetchone()

            if category_row:
                db.execute(
                    """
                    INSERT INTO products
                    (
                        name, category_id, price, image,
                        description, stock, delivery_time, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        category_row["id"],
                        price,
                        image,
                        description,
                        100,
                        "20-30 minutes",
                        now
                    )
                )

    db.commit()
    db.close()

# ============================================================
# AUTH
# ============================================================

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper


def location_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        if not session.get("user_location"):
            return redirect(url_for("location"))

        return function(*args, **kwargs)
    return wrapper

# ============================================================
# CART - DATABASE BASED
# ============================================================

def get_cart():
    """Return the logged-in user's cart as {product_id: quantity}."""
    if "user_id" not in session:
        return {}

    db = get_db()

    rows = db.execute(
        """
        SELECT product_id, quantity
        FROM cart_items
        WHERE user_id=?
        """,
        (session["user_id"],)
    ).fetchall()

    db.close()

    cart = {}

    for row in rows:
        try:
            product_id = str(int(row["product_id"]))
            quantity = int(row["quantity"])

            if quantity > 0:
                cart[product_id] = quantity
        except (ValueError, TypeError):
            pass

    return cart


def cart_count():
    """Number of products/units currently in the user's cart."""
    if "user_id" not in session:
        return 0

    db = get_db()

    row = db.execute(
        """
        SELECT COALESCE(SUM(quantity), 0) AS total
        FROM cart_items
        WHERE user_id=?
        """,
        (session["user_id"],)
    ).fetchone()

    db.close()

    return int(row["total"] or 0)

# ============================================================
# TEMPLATE GLOBALS
# ============================================================

@app.context_processor
def globals_for_templates():
    return {
        "cart_count": cart_count(),
        "user_location": session.get("user_location"),
        "current_user_name": session.get("user_name"),
        "logged_in": "user_id" in session
    }

# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if not session.get("user_location"):
        return redirect(url_for("location"))

    return redirect(url_for("home"))


@app.route("/home")
@location_required
def home():
    db = get_db()

    categories = db.execute(
        """
        SELECT id, name
        FROM categories
        ORDER BY id
        """
    ).fetchall()

    products = db.execute(
        """
        SELECT
            p.id,
            p.name,
            p.category_id,
            c.name AS category,
            p.price,
            p.image,
            p.description,
            p.stock,
            p.delivery_time,
            p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id=c.id
        ORDER BY p.id DESC
        LIMIT 12
        """
    ).fetchall()

    db.close()

    return render_template(
        "home.html",
        products=products,
        categories=categories
    )

# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter email and password.", "danger")
            return redirect(url_for("login"))

        db = get_db()

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE LOWER(email)=?
            AND password=?
            """,
            (email, password)
        ).fetchone()

        db.close()

        if user:
            # Keep any session cart, then restore it.
            old_session_cart = session.get("cart", {})

            if not isinstance(old_session_cart, dict):
                old_session_cart = {}

            session.clear()

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["user_location"] = user["location"] or ""

            # Compatibility with older session carts.
            session["cart"] = old_session_cart

            # If an old session cart exists, move it into DB.
            if old_session_cart:
                db = get_db()

                for product_id, quantity in old_session_cart.items():
                    try:
                        pid = int(product_id)
                        qty = int(quantity)

                        if qty > 0:
                            db.execute(
                                """
                                INSERT INTO cart_items
                                (user_id, product_id, quantity)
                                VALUES (?, ?, ?)
                                ON CONFLICT(user_id, product_id)
                                DO UPDATE SET quantity=quantity+excluded.quantity
                                """,
                                (
                                    user["id"],
                                    pid,
                                    qty
                                )
                            )
                    except (ValueError, TypeError):
                        pass

                db.commit()
                db.close()

                session["cart"] = {}
                session.modified = True

            if user["location"]:
                return redirect(url_for("home"))

            return redirect(url_for("location"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")

# ============================================================
# SIGNUP
# ============================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "").strip()
        address = request.form.get("address", "").strip()

        if not name or not email or not password:
            flash(
                "Name, email and password are required.",
                "danger"
            )
            return redirect(url_for("signup"))

        db = get_db()

        try:
            db.execute(
                """
                INSERT INTO users
                (
                    name, email, phone, password,
                    address, location, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    phone,
                    password,
                    address,
                    "",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )

            db.commit()

        except sqlite3.IntegrityError:
            db.close()
            flash(
                "Email already registered. Please login.",
                "danger"
            )
            return redirect(url_for("login"))

        db.close()

        flash(
            "Account created successfully. Please login.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("signup.html")

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ============================================================
# LOCATION
# ============================================================

@app.route("/location", methods=["GET", "POST"])
@login_required
def location():
    if request.method == "POST":
        user_location = request.form.get(
            "location", ""
        ).strip()

        address = request.form.get(
            "address", ""
        ).strip()

        if not user_location:
            flash(
                "Please enter your delivery location.",
                "danger"
            )
            return redirect(url_for("location"))

        db = get_db()

        db.execute(
            """
            UPDATE users
            SET location=?, address=?
            WHERE id=?
            """,
            (
                user_location,
                address,
                session["user_id"]
            )
        )

        db.commit()
        db.close()

        session["user_location"] = user_location
        session.modified = True

        return redirect(url_for("home"))

    return render_template("location.html")

# ============================================================
# BASIC PAGES
# ============================================================

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/delivery")
def delivery():
    return render_template("Delivery.html")

# ============================================================
# PRODUCT HELPERS
# ============================================================

def get_all_products():
    db = get_db()

    products = db.execute(
        """
        SELECT
            p.id,
            p.name,
            p.category_id,
            c.name AS category,
            p.price,
            p.image,
            p.description,
            p.stock,
            p.delivery_time,
            p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id=c.id
        ORDER BY p.name
        """
    ).fetchall()

    db.close()
    return products


def get_single_product(product_id):
    db = get_db()

    product = db.execute(
        """
        SELECT
            p.id,
            p.name,
            p.category_id,
            c.name AS category,
            p.price,
            p.image,
            p.description,
            p.stock,
            p.delivery_time,
            p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id=c.id
        WHERE p.id=?
        """,
        (product_id,)
    ).fetchone()

    db.close()
    return product


def get_category_products(category_name):
    db = get_db()

    products = db.execute(
        """
        SELECT
            p.id,
            p.name,
            p.category_id,
            c.name AS category,
            p.price,
            p.image,
            p.description,
            p.stock,
            p.delivery_time,
            p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id=c.id
        WHERE LOWER(c.name)=LOWER(?)
        ORDER BY p.name
        """,
        (category_name,)
    ).fetchall()

    db.close()
    return products

# ============================================================
# PRODUCTS
# ============================================================

@app.route("/products")
@location_required
def products():
    return render_template(
        "products.html",
        products=get_all_products()
    )


@app.route("/product/<int:product_id>")
@location_required
def product(product_id):
    product_data = get_single_product(product_id)

    if not product_data:
        flash("Product not found.", "danger")
        return redirect(url_for("products"))

    return render_template(
        "productDetails.html",
        product=product_data
    )

# ============================================================
# CATEGORY PAGES
# ============================================================

@app.route("/seeds")
@location_required
def seeds():
    return render_template(
        "seeds.html",
        products=get_category_products("Seeds")
    )


@app.route("/fertilizer")
@location_required
def fertilizer():
    return render_template(
        "Fertilizer.html",
        products=get_category_products("Fertilizer")
    )


@app.route("/tools")
@location_required
def tools():
    return render_template(
        "tools.html",
        products=get_category_products("Tools")
    )


@app.route("/equipment")
@location_required
def equipment():
    return render_template(
        "equipment.html",
        products=get_category_products("Equipment")
    )


@app.route("/crop-care")
@location_required
def crop_care():
    return render_template(
        "crop_care.html",
        products=get_category_products("Cropcare")
    )

# ============================================================
# CATEGORY REDIRECT
# ============================================================

@app.route("/category/<category_name>")
@location_required
def category(category_name):
    name = category_name.lower().strip()

    mapping = {
        "seeds": "seeds",
        "fertilizer": "fertilizer",
        "fertilizers": "fertilizer",
        "tools": "tools",
        "equipment": "equipment",
        "cropcare": "crop_care",
        "crop-care": "crop_care",
        "crop care": "crop_care",
        "irrigation": "products",
        "pesticides": "products",
        "organic farming": "products",
        "nursery": "products",
        "animal farming": "products"
    }

    if name in mapping:
        return redirect(url_for(mapping[name]))

    return redirect(url_for("products"))

# ============================================================
# SEARCH
# ============================================================

@app.route("/search")
@location_required
def search():
    query = request.args.get("q", "").strip()

    db = get_db()

    if query:
        products_list = db.execute(
            """
            SELECT
                p.id,
                p.name,
                p.category_id,
                c.name AS category,
                p.price,
                p.image,
                p.description,
                p.stock,
                p.delivery_time,
                p.created_at
            FROM products p
            LEFT JOIN categories c ON p.category_id=c.id
            WHERE p.name LIKE ?
               OR c.name LIKE ?
               OR p.description LIKE ?
            ORDER BY p.name
            """,
            (
                f"%{query}%",
                f"%{query}%",
                f"%{query}%"
            )
        ).fetchall()
    else:
        products_list = []

    db.close()

    return render_template(
        "search.html",
        products=products_list,
        search_query=query
    )

# ============================================================
# ADD TO CART
# ============================================================

def add_item(product_id, quantity=1):
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    if not product_id:
        flash("Invalid product.", "danger")
        return redirect(url_for("products"))

    db = get_db()

    product_data = db.execute(
        """
        SELECT *
        FROM products
        WHERE id=?
        """,
        (product_id,)
    ).fetchone()

    if not product_data:
        db.close()
        flash("Product not found.", "danger")
        return redirect(url_for("products"))

    stock = int(product_data["stock"] or 0)

    if stock <= 0:
        db.close()
        flash("Product is out of stock.", "warning")
        return redirect(url_for("products"))

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    existing = db.execute(
        """
        SELECT quantity
        FROM cart_items
        WHERE user_id=?
        AND product_id=?
        """,
        (
            session["user_id"],
            product_id
        )
    ).fetchone()

    if existing:
        old_quantity = int(existing["quantity"])
        new_quantity = old_quantity + quantity

        if new_quantity > stock:
            new_quantity = stock

        db.execute(
            """
            UPDATE cart_items
            SET quantity=?
            WHERE user_id=?
            AND product_id=?
            """,
            (
                new_quantity,
                session["user_id"],
                product_id
            )
        )
    else:
        if quantity > stock:
            quantity = stock

        db.execute(
            """
            INSERT INTO cart_items
            (
                user_id,
                product_id,
                quantity
            )
            VALUES (?, ?, ?)
            """,
            (
                session["user_id"],
                product_id,
                quantity
            )
        )

    db.commit()
    db.close()

    flash(
        product_data["name"] + " added to cart.",
        "success"
    )

    return redirect(url_for("cart"))


@app.route("/add-to-cart", methods=["POST"])
@location_required
def add_to_cart_post():
    product_id = request.form.get(
        "product_id",
        type=int
    )

    quantity = request.form.get(
        "quantity",
        1,
        type=int
    )

    return add_item(product_id, quantity)


@app.route("/add-to-cart/<int:product_id>")
@location_required
def add_to_cart(product_id):
    return add_item(product_id, 1)

# ============================================================
# CART PAGE
# ============================================================

@app.route("/cart")
@location_required
def cart():
    user_id = session["user_id"]

    db = get_db()

    rows = db.execute(
        """
        SELECT
            p.id,
            p.name,
            p.price,
            p.image,
            p.stock,
            p.delivery_time,
            ci.quantity
        FROM cart_items ci
        JOIN products p ON ci.product_id=p.id
        WHERE ci.user_id=?
        ORDER BY ci.id DESC
        """,
        (user_id,)
    ).fetchall()

    items = []
    total = 0

    for row in rows:
        quantity = int(row["quantity"])
        stock = int(row["stock"] or 0)

        if stock <= 0:
            db.execute(
                """
                DELETE FROM cart_items
                WHERE user_id=? AND product_id=?
                """,
                (user_id, row["id"])
            )
            continue

        if quantity > stock:
            quantity = stock

            db.execute(
                """
                UPDATE cart_items
                SET quantity=?
                WHERE user_id=? AND product_id=?
                """,
                (
                    quantity,
                    user_id,
                    row["id"]
                )
            )

        subtotal = float(row["price"]) * quantity
        total += subtotal

        items.append({
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "image": row["image"],
            "quantity": quantity,
            "subtotal": subtotal,
            "delivery_time":
                row["delivery_time"] or "20-30 minutes"
        })

    db.commit()
    db.close()

    return render_template(
        "cart.html",
        items=items,
        total=total
    )

# ============================================================
# INCREASE
# ============================================================

@app.route("/increase/<int:product_id>")
@location_required
def increase(product_id):
    user_id = session["user_id"]

    db = get_db()

    row = db.execute(
        """
        SELECT
            ci.quantity,
            p.stock
        FROM cart_items ci
        JOIN products p ON ci.product_id=p.id
        WHERE ci.user_id=?
        AND ci.product_id=?
        """,
        (
            user_id,
            product_id
        )
    ).fetchone()

    if row:
        current = int(row["quantity"])
        stock = int(row["stock"] or 0)

        if current < stock:
            db.execute(
                """
                UPDATE cart_items
                SET quantity=quantity+1
                WHERE user_id=? AND product_id=?
                """,
                (
                    user_id,
                    product_id
                )
            )

    db.commit()
    db.close()

    return redirect(url_for("cart"))

# ============================================================
# DECREASE
# ============================================================

@app.route("/decrease/<int:product_id>")
@location_required
def decrease(product_id):
    user_id = session["user_id"]

    db = get_db()

    row = db.execute(
        """
        SELECT quantity
        FROM cart_items
        WHERE user_id=? AND product_id=?
        """,
        (
            user_id,
            product_id
        )
    ).fetchone()

    if row:
        quantity = int(row["quantity"])

        if quantity > 1:
            db.execute(
                """
                UPDATE cart_items
                SET quantity=quantity-1
                WHERE user_id=? AND product_id=?
                """,
                (
                    user_id,
                    product_id
                )
            )
        else:
            db.execute(
                """
                DELETE FROM cart_items
                WHERE user_id=? AND product_id=?
                """,
                (
                    user_id,
                    product_id
                )
            )

    db.commit()
    db.close()

    return redirect(url_for("cart"))

# ============================================================
# REMOVE
# ============================================================

@app.route("/remove-from-cart/<int:product_id>")
@location_required
def remove_from_cart(product_id):
    db = get_db()

    db.execute(
        """
        DELETE FROM cart_items
        WHERE user_id=? AND product_id=?
        """,
        (
            session["user_id"],
            product_id
        )
    )

    db.commit()
    db.close()

    flash("Product removed from cart.", "success")

    return redirect(url_for("cart"))

# ============================================================
# CHECKOUT
# ============================================================

@app.route("/checkout", methods=["GET", "POST"])
@location_required
def checkout():
    user_id = session["user_id"]

    db = get_db()

    cart_rows = db.execute(
        """
        SELECT
            p.*,
            ci.quantity
        FROM cart_items ci
        JOIN products p ON ci.product_id=p.id
        WHERE ci.user_id=?
        """,
        (user_id,)
    ).fetchall()

    items = []
    total = 0

    for product_data in cart_rows:
        quantity = int(product_data["quantity"])
        stock = int(product_data["stock"] or 0)

        if stock <= 0:
            continue

        if quantity > stock:
            quantity = stock

        subtotal = float(product_data["price"]) * quantity
        total += subtotal

        items.append(
            (
                product_data,
                quantity,
                subtotal
            )
        )

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE id=?
        """,
        (user_id,)
    ).fetchone()

    if not items:
        db.close()

        flash("Your cart is empty.", "warning")

        return redirect(url_for("products"))

    if request.method == "POST":
        customer_name = request.form.get(
            "customer_name",
            request.form.get("name", "")
        ).strip()

        phone = request.form.get(
            "phone",
            request.form.get("mobile", "")
        ).strip()

        address = request.form.get(
            "address", ""
        ).strip()

        if not customer_name and user:
            customer_name = user["name"] or ""

        if not phone and user:
            phone = user["phone"] or ""

        if not address and user:
            address = user["address"] or ""

        if not customer_name:
            db.close()
            flash("Please enter your name.", "danger")
            return redirect(url_for("checkout"))

        if not phone:
            db.close()
            flash("Please enter your mobile number.", "danger")
            return redirect(url_for("checkout"))

        if not address:
            db.close()
            flash("Please enter your delivery address.", "danger")
            return redirect(url_for("checkout"))

        # STOCK CHECK
        for product_data, quantity, subtotal in items:
            if int(product_data["stock"] or 0) < quantity:
                db.close()

                flash(
                    "Insufficient stock for "
                    + product_data["name"],
                    "danger"
                )

                return redirect(url_for("cart"))

        cursor = db.cursor()

        # CREATE ORDER
        cursor.execute(
            """
            INSERT INTO orders
            (
                user_id,
                customer_name,
                phone,
                address,
                total,
                status,
                delivery_time,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                customer_name,
                phone,
                address,
                total,
                "Order Placed",
                "20-30 minutes",
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        order_id = cursor.lastrowid

        # ORDER ITEMS + STOCK
        for product_data, quantity, subtotal in items:
            cursor.execute(
                """
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    product_name,
                    quantity,
                    price,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    product_data["id"],
                    product_data["name"],
                    quantity,
                    product_data["price"],
                    subtotal
                )
            )

            cursor.execute(
                """
                UPDATE products
                SET stock=stock-?
                WHERE id=?
                """,
                (
                    quantity,
                    product_data["id"]
                )
            )

        # CLEAR DATABASE CART ONLY AFTER SUCCESSFUL ORDER
        cursor.execute(
            """
            DELETE FROM cart_items
            WHERE user_id=?
            """,
            (user_id,)
        )

        db.commit()
        db.close()

        # Clear old session-cart compatibility data too.
        session["cart"] = {}
        session.modified = True

        flash(
            "Order placed successfully! "
            "Delivery in 20-30 minutes.",
            "success"
        )

        return redirect(url_for("orders"))

    simple_items = []

    for product_data, quantity, subtotal in items:
        simple_items.append({
            "id": product_data["id"],
            "name": product_data["name"],
            "price": product_data["price"],
            "image": product_data["image"],
            "quantity": quantity,
            "subtotal": subtotal
        })

    db.close()

    return render_template(
        "checkout.html",
        items=simple_items,
        total=total,
        user=user
    )

# ============================================================
# ORDERS
# ============================================================

@app.route("/orders")
@location_required
def orders():
    db = get_db()

    orders_list = db.execute(
        """
        SELECT *
        FROM orders
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    db.close()

    return render_template(
        "orders.html",
        orders=orders_list
    )


@app.route("/order/<int:order_id>")
@location_required
def order_detail(order_id):
    db = get_db()

    order = db.execute(
        """
        SELECT *
        FROM orders
        WHERE id=?
        AND user_id=?
        """,
        (
            order_id,
            session["user_id"]
        )
    ).fetchone()

    if not order:
        db.close()

        flash("Order not found.", "danger")

        return redirect(url_for("orders"))

    order_items = db.execute(
        """
        SELECT *
        FROM order_items
        WHERE order_id=?
        """,
        (order_id,)
    ).fetchall()

    db.close()

    return render_template(
        "orders.html",
        orders=[order],
        order_items=order_items,
        selected_order=order
    )

# ============================================================
# PROFILE
# ============================================================

@app.route("/profile", methods=["GET", "POST"])
@location_required
def profile():
    db = get_db()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE id=?
        """,
        (session["user_id"],)
    ).fetchone()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        user_location = request.form.get("location", "").strip()

        db.execute(
            """
            UPDATE users
            SET name=?, phone=?, address=?, location=?
            WHERE id=?
            """,
            (
                name,
                phone,
                address,
                user_location,
                session["user_id"]
            )
        )

        db.commit()
        db.close()

        session["user_name"] = name
        session["user_location"] = user_location
        session.modified = True

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(url_for("home"))

    db.close()

    return render_template(
        "profile.html",
        user=user
    )

# ============================================================
# API
# ============================================================

@app.route("/api/cart-count")
def api_cart_count():
    return jsonify(
        success=True,
        count=cart_count()
    )


@app.route("/api/products")
def api_products():
    products_list = get_all_products()

    return jsonify(
        success=True,
        products=[
            dict(product)
            for product in products_list
        ]
    )


@app.route("/api/product/<int:product_id>")
def api_product(product_id):
    product_data = get_single_product(product_id)

    if product_data:
        return jsonify(
            success=True,
            product=dict(product_data)
        )

    return jsonify(
        success=False,
        message="Product not found"
    ), 404


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()

    db = get_db()

    if query:
        products_list = db.execute(
            """
            SELECT
                p.id,
                p.name,
                p.category_id,
                c.name AS category,
                p.price,
                p.image,
                p.description,
                p.stock,
                p.delivery_time,
                p.created_at
            FROM products p
            LEFT JOIN categories c ON p.category_id=c.id
            WHERE p.name LIKE ?
               OR c.name LIKE ?
               OR p.description LIKE ?
            ORDER BY p.name
            """,
            (
                f"%{query}%",
                f"%{query}%",
                f"%{query}%"
            )
        ).fetchall()
    else:
        products_list = []

    db.close()

    return jsonify(
        success=True,
        products=[
            dict(product)
            for product in products_list
        ]
    )


@app.route("/api/categories")
def api_categories():
    db = get_db()

    categories_list = db.execute(
        """
        SELECT id, name
        FROM categories
        ORDER BY id
        """
    ).fetchall()

    db.close()

    return jsonify(
        success=True,
        categories=[
            dict(category)
            for category in categories_list
        ]
    )


@app.route("/api/delivery-info")
def delivery_info():
    return jsonify(
        success=True,
        available=True,
        delivery_time="20-30 minutes",
        location=session.get("user_location", "")
    )

# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():
    return jsonify(
        status="OK",
        application="AgroQuick",
        delivery="20-30 minutes"
    )

# ============================================================
# START DATABASE
# ============================================================

init_db()

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )

