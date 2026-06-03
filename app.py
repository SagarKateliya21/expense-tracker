import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Name is required.")
    if not email:
        return render_template("register.html", error="Email address is required.")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    password_hash = generate_password_hash(password)
    try:
        create_user(name, email, password_hash)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists.")

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    flash("Welcome back, {}!".format(user["name"]), "success")
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You've been signed out.", "success")
    return redirect(url_for("landing"))


@app.route("/dashboard")
def dashboard():
    return "Dashboard — coming soon"


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user = {
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "member_since": "January 2025",
    }
    stats = {
        "total_spent": "₹6,340",
        "transaction_count": 8,
        "top_category": "Shopping",
    }
    transactions = [
        {"date": "10 Jun 2026", "description": "Clothing",            "category": "Shopping",      "amount": "₹2,500"},
        {"date": "03 Jun 2026", "description": "Electricity bill",    "category": "Bills",         "amount": "₹1,200"},
        {"date": "05 Jun 2026", "description": "Pharmacy",            "category": "Health",        "amount": "₹800"},
        {"date": "12 Jun 2026", "description": "Miscellaneous",       "category": "Other",         "amount": "₹600"},
        {"date": "01 Jun 2026", "description": "Lunch at cafe",       "category": "Food",          "amount": "₹450"},
        {"date": "08 Jun 2026", "description": "Movie tickets",       "category": "Entertainment", "amount": "₹350"},
        {"date": "15 Jun 2026", "description": "Groceries",           "category": "Food",          "amount": "₹320"},
        {"date": "02 Jun 2026", "description": "Metro card recharge", "category": "Transport",     "amount": "₹120"},
    ]
    categories = [
        {"name": "Shopping",      "amount": "₹2,500", "pct": 39},
        {"name": "Bills",         "amount": "₹1,200", "pct": 19},
        {"name": "Health",        "amount": "₹800",   "pct": 13},
        {"name": "Food",          "amount": "₹770",   "pct": 12},
        {"name": "Other",         "amount": "₹600",   "pct": 9},
        {"name": "Entertainment", "amount": "₹350",   "pct": 6},
        {"name": "Transport",     "amount": "₹120",   "pct": 2},
    ]
    return render_template("profile.html", user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
