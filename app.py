from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)

@app.route("/")
def home():
    return render_template(
        "homepage.html"
    )
@app.route("/election_sim", methods = ['GET'])
def election_app():
    return render_template(
        "election_sim.html"
    )
@app.route('/election_sim/submission', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.instance_path, 'uploads', secure_filename(f.filename)))
        return render_template(
            "submission.html", filename = f.filename, type = "file"
        )
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html')

@app.errorhandler(400)
def page_not_found(error):
   return render_template('400.html')

if __name__ == "__main__" :
    app.run()
