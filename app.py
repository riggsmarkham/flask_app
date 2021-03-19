from flask import Flask
from datetime import datetime
from flask import render_template
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "first_page.html"
    )