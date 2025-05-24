from flask import Flask, render_template, request, flash, redirect, session
import sqlite3
import secrets
import users
import config

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    listings = []
    return render_template("index.html",  listings=listings)


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
