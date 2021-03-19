from flask import Flask
from datetime import datetime
from flask import render_template
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "first_page.html",
        name=name,
        date=datetime.now()
    )