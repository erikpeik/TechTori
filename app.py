from flask import Flask, abort, render_template, request, flash, redirect, session
import sqlite3
import secrets
import users
import config
import categories
import conditions
import listings

app = Flask(__name__)
app.secret_key = config.secret_key


def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/")
def index():
    listings_list = listings.get_listings()
    return render_template("index.html",  listings=listings_list)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        print(password, password_confirm)
        if password != password_confirm:
            flash("Virhe: Salasanat eivät täsmää", "error")
            return redirect("/register")

        try:
            user_id = users.create_user(username, password)
            flash("Käyttäjä luotu onnistuneesti", "success")
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)

        except sqlite3.IntegrityError:
            flash("Virhe: Käyttäjätunnus on jo käytössä", "error")
            return redirect("/register")

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(username, password)

        user_id = users.authenticate_user(username, password)
        if user_id is None:
            flash("Virhe: Väärä käyttäjätunnus tai salasana", "error")
            return redirect("/login")

        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


@app.route("/create-item", methods=["GET", "POST"])
def create_item():
    require_login()
    if request.method == "GET":
        categories_list = categories.get_categories()
        conditions_list = conditions.get_conditions()
        return render_template("create-item.html", categories=categories_list, conditions=conditions_list)
    if request.method == "POST":
        check_csrf()
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        condition_id = request.form.get("condition")
        category_id = request.form.get("category")

        if not title or not description or not price or not condition_id or not category_id:
            flash("Virhe: Kaikki kentät ovat pakollisia", "error")
            return redirect("/create-item")

        print("user_id:", session["user_id"])
        print("condition_id:", condition_id)
        print("category_id:", category_id)
        try:
            listings.add_listing(
                session["user_id"], title, description, price, condition_id, category_id)
        except sqlite3.IntegrityError:
            flash("Virhe: Ilmoituksen luominen epäonnistui", "error")
            return redirect("/create-item")
        flash("Ilmoitus luotu onnistuneesti", "success")
        return redirect("/")

@app.route("/listing/<int:listing_id>")
def listing_detail(listing_id):
    listing = listings.get_listing(listing_id)
    if not listing:
        abort(404)
    return render_template("listing.html", listing=listing)
