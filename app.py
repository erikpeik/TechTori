from flask import Flask, abort, render_template, request, flash, redirect, session
import secrets
import re
import users
import config
import categories
import conditions
import listings
import favorites

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
    favorites_list = favorites.get_favorited_ids()

    listings_list = [dict(listing) for listing in listings_list]
    for listing in listings_list:
        listing["is_favorited"] = listing["id"] in favorites_list

    return render_template("index.html",  listings=listings_list)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if not username or not password or not password_confirm:
            flash("Virhe: Kaikki kentät ovat pakollisia", "error")
            return redirect("/register")

        if not (3 <= len(username) <= 20):
            flash("Virhe: Käyttäjätunnuksen tulee olla 3-20 merkkiä pitkä", "error")
            return redirect("/register")

        if password != password_confirm:
            flash("Virhe: Salasanat eivät täsmää", "error")
            return redirect("/register")

        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            flash(
                "Virhe: Salasanan tulee olla vähintään 8 merkkiä ja sisältää kirjaimia sekä numeroita.", "error")
            return redirect("/register")

        # check if user already exists
        if users.get_user_by_username(username):
            flash("Virhe: Käyttäjätunnus on jo käytössä", "error")
            return redirect("/register")

        user_id = users.create_user(username, password)
        flash("Käyttäjä luotu onnistuneesti", "success")
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

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

        if len(title) > 100:
            flash("Virhe: Otsikon maksimipituus on 100 merkkiä", "error")
            return redirect("/create-item")

        if len(description) > 1000:
            flash("Virhe: Kuvauksen maksimipituus on 1000 merkkiä", "error")
            return redirect("/create-item")

        if int(price) < 0 or int(price) > 10000:
            flash("Virhe: Hinta ei voi olla negatiivinen tai yli 10 000€", "error")
            return redirect("/create-item")

        condition = conditions.get_condition_by_id(condition_id)
        category = categories.get_category_by_id(category_id)

        if not condition or not category:
            flash("Virhe: Valittu kunto tai kategoria on virheellinen", "error")
            return redirect("/create-item")

        listings.add_listing(
            session["user_id"], title, description, price, condition_id, category_id)

        flash("Ilmoitus luotu onnistuneesti", "success")
        return redirect("/")


@app.route("/listing/<int:listing_id>")
def listing_detail(listing_id):
    listing = listings.get_listing(listing_id)
    is_favorited = favorites.is_favorited(listing_id)
    if not listing:
        abort(404)
    return render_template("listing.html", listing=listing, is_favorited=is_favorited)


@app.route("/edit-listing/<int:listing_id>", methods=["GET", "POST"])
def edit_listing(listing_id):
    require_login()
    if request.method == "GET":
        listing = listings.get_listing(listing_id)
        if not listing or listing["user_id"] != session["user_id"]:
            abort(403)
        categories_list = categories.get_categories()
        conditions_list = conditions.get_conditions()
        return render_template("edit-listing.html", listing=listing, categories=categories_list, conditions=conditions_list)

    if request.method == "POST":
        check_csrf()
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        condition_id = request.form.get("condition")
        category_id = request.form.get("category")

        if not title or not description or not price or not condition_id or not category_id:
            flash("Virhe: Kaikki kentät ovat pakollisia", "error")
            return redirect(f"/edit-listing/{listing_id}")

        if len(title) > 100:
            flash("Virhe: Otsikon maksimipituus on 100 merkkiä", "error")
            return redirect(f"/edit-listing/{listing_id}")

        if len(description) > 1000:
            flash("Virhe: Kuvauksen maksimipituus on 1000 merkkiä", "error")
            return redirect(f"/edit-listing/{listing_id}")

        if int(price) < 0 or int(price) > 10000:
            flash("Virhe: Hinta ei voi olla negatiivinen tai yli 10 000€", "error")
            return redirect(f"/edit-listing/{listing_id}")

        condition = conditions.get_condition_by_id(condition_id)
        category = categories.get_category_by_id(category_id)

        if not condition or not category:
            flash("Virhe: Valittu kunto tai kategoria on virheellinen", "error")
            return redirect(f"/edit-listing/{listing_id}")

        listings.update_listing(
            listing_id, title, description, price, condition_id, category_id)

        flash("Ilmoitus päivitetty onnistuneesti", "success")

        return redirect(f"/listing/{listing_id}")


@app.route("/delete-listing/<int:listing_id>", methods=["GET", "POST"])
def delete_listing(listing_id):
    require_login()
    if request.method == "GET":
        listing = listings.get_listing(listing_id)
        if not listing or listing["user_id"] != session["user_id"]:
            abort(403)
        return render_template("delete-listing.html", listing=listing)

    if request.method == "POST":
        check_csrf()
        listings.delete_listing(listing_id)
        flash("Ilmoitus poistettu onnistuneesti", "success")
        return redirect("/profile")


@app.route("/profile")
def profile():
    require_login()
    user_id = session["user_id"]
    user_info = users.get_user_info(user_id)
    user_listings = listings.get_user_listings(user_id)
    return render_template("profile.html", user=user_info, listings=user_listings)


@app.route("/profile/<int:user_id>")
def user_profile(user_id):
    user_info = users.get_user_info(user_id)
    if not user_info:
        abort(404)
    user_listings = listings.get_user_listings(user_id)
    return render_template("profile.html", user=user_info, listings=user_listings)


@app.route("/favorite/<int:listing_id>", methods=["POST"])
def favorite_listing(listing_id):
    require_login()
    check_csrf()
    redirect_url = request.form.get("redirect", "/")

    if favorites.is_favorited(listing_id):
        favorites.remove_favorite(listing_id)
        flash("Ilmoitus poistettu suosikeista", "success")
    else:
        favorites.add_favorite(listing_id)
        flash("Ilmoitus lisätty suosikkeihin", "success")

    return redirect(redirect_url)


@app.route("/buy-listing/<int:listing_id>", methods=["POST"])
def buy_listing(listing_id):
    require_login()
    check_csrf()

    listings.mark_listing_as_sold(listing_id)
    flash("Ilmoitus merkitty myydyksi", "success")

    return redirect(f"/listing/{listing_id}")
