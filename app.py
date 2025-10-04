import re
import secrets
import math
from urllib.parse import urlencode
from flask import Flask, abort, render_template, request, flash, redirect, session
import markupsafe
import users
import config
import categories
import conditions
import listings
import favorites

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


@app.template_filter()
def show_short_content(content):
    text = str(show_lines(content))
    lines = text.split("<br />")
    text = "<br />".join(lines[:5])
    if len(text) > 150:
        text = text[:150]
    if len(lines) > 5 or len(text) >= 150:
        text += "..."

    return markupsafe.Markup(text)


@app.template_filter()
def pagination_url(page_num):
    args = request.args.copy()
    args['page'] = page_num
    return f"{request.path}?{urlencode(args)}"


@app.route("/")
def index():
    search = request.args.get("search")
    category = request.args.get("category")
    condition = request.args.get("condition")
    exclude_own = request.args.get("exclude-own") == "on"
    page = request.args.get("page", 1, type=int)

    listing_count = listings.listing_count(
        search, category, condition, exclude_own)
    page_size = 10
    page_count = max(math.ceil(listing_count / page_size), 1)

    if page < 1:
        return redirect(pagination_url(1))
    if page > page_count:
        return redirect(pagination_url(page_count))

    listings_list = listings.get_listings(
        search,
        category,
        condition,
        exclude_own,
        page=page,
        page_size=page_size
    )
    categories_list = categories.get_categories()
    conditions_list = conditions.get_conditions()
    return render_template(
        "index.html",
        listings=listings_list,
        categories=categories_list,
        conditions=conditions_list,
        page=page,
        page_count=page_count,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # POST method
    username = request.form.get("username")
    password = request.form.get("password")
    password_confirm = request.form.get("password_confirm")

    error_msg = None

    if not username or not password or not password_confirm:
        error_msg = "Virhe: Kaikki kentät ovat pakollisia"
    elif not 3 <= len(username) <= 20:
        error_msg = "Virhe: Käyttäjätunnuksen tulee olla 3-20 merkkiä pitkä"
    elif password != password_confirm:
        error_msg = "Virhe: Salasanat eivät täsmää"
    elif not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        error_msg = (
            "Virhe: Salasanan tulee olla vähintään 8 merkkiä ja "
            "sisältää kirjaimia sekä numeroita."
        )
    elif users.get_user_by_username(username):
        error_msg = "Virhe: Käyttäjätunnus on jo käytössä"

    if error_msg:
        flash(error_msg, "error")
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

    # POST method
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
        return render_template("create-item.html",
                               categories=categories_list,
                               conditions=conditions_list)

    # POST method

    check_csrf()
    title = request.form.get("title")
    description = request.form.get("description")
    price = request.form.get("price")
    condition_id = request.form.get("condition")
    category_id = request.form.get("category")

    error_msg = None

    if not title or not price or not condition_id or not category_id:
        error_msg = "Virhe: Pakolliset kentät puuttuvat"
    elif len(title) > 100:
        error_msg = "Virhe: Otsikon maksimipituus on 100 merkkiä"
    elif len(description) > 1000:
        error_msg = "Virhe: Kuvauksen maksimipituus on 1000 merkkiä"
    elif int(price) < 0 or int(price) > 10000:
        error_msg = "Virhe: Hinta ei voi olla negatiivinen tai yli 10 000€"
    elif not conditions.get_condition_by_id(condition_id) \
            or not categories.get_category_by_id(category_id):
        error_msg = "Virhe: Valittu kunto tai kategoria on virheellinen"

    if error_msg:
        flash(error_msg, "error")
        return redirect("/create-item")

    listings.add_listing(
        session["user_id"],
        title=title,
        description=description,
        price=price,
        condition_id=condition_id,
        category_id=category_id
    )

    flash("Ilmoitus luotu onnistuneesti", "success")
    return redirect("/")


@app.route("/listing/<int:listing_id>")
def listing_detail(listing_id):
    listing = listings.get_listing(listing_id)
    is_favorited = favorites.is_favorited(listing_id)
    is_sold = listings.is_listing_sold(listing_id)
    if not listing:
        abort(404)
    return render_template("listing.html",
                           listing=listing,
                           is_favorited=is_favorited,
                           is_sold=is_sold)


@app.route("/edit-listing/<int:listing_id>", methods=["GET", "POST"])
def edit_listing(listing_id):
    require_login()
    if request.method == "GET":
        listing = listings.get_listing(listing_id)
        if not listing or listing["user_id"] != session["user_id"]:
            abort(403)
        categories_list = categories.get_categories()
        conditions_list = conditions.get_conditions()
        return render_template("edit-listing.html",
                               listing=listing,
                               categories=categories_list,
                               conditions=conditions_list
                               )

    # POST method
    check_csrf()
    title = request.form.get("title")
    description = request.form.get("description")
    price = request.form.get("price")
    condition_id = request.form.get("condition")
    category_id = request.form.get("category")

    error_msg = None

    if not title or not price or not condition_id or not category_id:
        error_msg = "Virhe: Pakolliset kentät puuttuvat"
    elif len(title) > 100:
        error_msg = "Virhe: Otsikon maksimipituus on 100 merkkiä"
    elif len(description) > 1000:
        error_msg = "Virhe: Kuvauksen maksimipituus on 1000 merkkiä"
    elif int(price) < 0 or int(price) > 10000:
        error_msg = "Virhe: Hinta ei voi olla negatiivinen tai yli 10 000€"
    elif not conditions.get_condition_by_id(condition_id) or \
            not categories.get_category_by_id(category_id):
        error_msg = "Virhe: Valittu kunto tai kategoria on virheellinen"

    if error_msg:
        flash(error_msg, "error")
        return redirect(f"/edit-listing/{listing_id}")

    listings.update_listing(
        listing_id,
        title=title,
        description=description,
        price=price,
        condition_id=condition_id,
        category_id=category_id
    )

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
        listing = listings.get_listing(listing_id)
        if not listing or listing["user_id"] != session["user_id"]:
            abort(403)

        listings.delete_listing(listing_id)
        flash("Ilmoitus poistettu onnistuneesti", "success")
        return redirect("/profile")
    return None


@app.route("/profile")
def profile():
    require_login()
    user_id = session["user_id"]
    user_info = users.get_user_info(user_id)
    listings_count = listings.get_user_listings_count(user_id)

    page = request.args.get("page", 1, type=int)

    page_size = 10
    page_count = max(math.ceil(listings_count / page_size), 1)

    if page < 1:
        return redirect("/profile")
    if page > page_count:
        return redirect(f"/profile?page={page_count}")

    user_listings = listings.get_user_listings(user_id, page, page_size)
    user_favorites = users.get_favorites(user_id)
    last_listing_date = listings.get_users_last_listing_created_at(user_id)

    return render_template("profile.html",
                           user=user_info,
                           listings=user_listings,
                           favorites=user_favorites,
                           listings_count=listings_count,
                           last_listing_date=last_listing_date,
                           page=page,
                           page_count=page_count
                           )


@app.route("/profile/<int:user_id>")
def user_profile(user_id):
    user_info = users.get_user_info(user_id)
    if not user_info:
        abort(404)
    listings_count = listings.get_user_listings_count(user_id)

    page = request.args.get("page", 1, type=int)

    page_size = 10
    page_count = max(math.ceil(listings_count / page_size), 1)

    if page < 1:
        return redirect(f"/profile/{user_id}")
    if page > page_count:
        return redirect(f"/profile/{user_id}?page={page_count}")

    user_listings = listings.get_user_listings(user_id, page, page_size)
    last_listing_date = listings.get_users_last_listing_created_at(user_id)

    return render_template("profile.html",
                           user=user_info,
                           listings=user_listings,
                           listings_count=listings_count,
                           last_listing_date=last_listing_date,
                           page=page,
                           page_count=page_count
                           )


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


@app.route("/unsell-listing/<int:listing_id>", methods=["POST"])
def unsell_listing(listing_id):
    require_login()
    check_csrf()

    listing = listings.get_listing(listing_id)

    if listing["user_id"] != session["user_id"]:
        abort(403)

    listings.mark_listing_as_unsold(listing_id)
    flash("Ilmoitus merkitty myynnistä poistettavaksi", "success")

    return redirect(f"/listing/{listing_id}")
