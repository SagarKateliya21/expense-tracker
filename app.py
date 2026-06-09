import sqlite3
from datetime import datetime
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database.db import (
    get_db, init_db, seed_db, create_user, get_user_by_email,
    get_user_by_id, get_expenses_by_user, get_expense_stats, get_category_breakdown,
)

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Formatting helpers                                                  #
# ------------------------------------------------------------------ #

def _fmt_inr(amount):
    return "₹{:,.0f}".format(amount)


def _fmt_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %b %Y")


def _fmt_member_since(created_at):
    return datetime.strptime(created_at[:19], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")


def _compute_pcts(rows):
    if not rows:
        return []
    grand = sum(r["total"] for r in rows)
    if grand == 0:
        return [0] * len(rows)
    floats = [r["total"] / grand * 100 for r in rows]
    floors = [int(f) for f in floats]
    diff = 100 - sum(floors)
    order = sorted(range(len(floats)), key=lambda i: floats[i] - floors[i], reverse=True)
    for i in range(diff):
        floors[order[i]] += 1
    return floors


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

    user_id = session["user_id"]

    raw_user = get_user_by_id(user_id)
    if raw_user is None:
        abort(404)

    user = {
        "name":         raw_user["name"],
        "email":        raw_user["email"],
        "member_since": _fmt_member_since(raw_user["created_at"]),
    }

    raw_txns = get_expenses_by_user(user_id)
    transactions = [
        {
            "date":        _fmt_date(row["date"]),
            "description": row["description"],
            "category":    row["category"],
            "amount":      _fmt_inr(row["amount"]),
        }
        for row in raw_txns
    ]

    raw_stats = get_expense_stats(user_id)
    stats = {
        "total_spent":       _fmt_inr(raw_stats["total_spent"]),
        "transaction_count": raw_stats["transaction_count"],
        "top_category":      raw_stats["top_category"] or "—",
    }

    raw_cats = get_category_breakdown(user_id)
    pcts = _compute_pcts(raw_cats)
    categories = [
        {
            "name":   row["category"],
            "amount": _fmt_inr(row["total"]),
            "pct":    pcts[i],
        }
        for i, row in enumerate(raw_cats)
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


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
