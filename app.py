from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    words = ["apina", "banaani", "cembalo"]
    return render_template("index.html", message="Tervetuloa!", items=words)
