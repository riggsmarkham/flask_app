from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "homepage.html"
    )
@app.route("/election_sim")
def election_app():
    return render_template(
        "election_sim.html"
    )