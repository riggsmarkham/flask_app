from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import sim

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
        sim.doAllSystems('Simulation', 'instance/uploads/' + f.filename, sim.NUM, False)
        return render_template(
            "submission.html", filename = f.filename, type = "file"
        )

# @app.route('/election_sim/result', methods = ['POST'])
# def run_sim():
#     if request.method == 'POST':
#         filename = request.form['filename']
#         doAllSystems('Simulation', 'instance/uploads/' + filename, NUM, False)
#         return render_template(
#             "result.html"
#         )

@app.errorhandler(404)
def page_not_found(error):
   return render_template('errors/404.html')

@app.errorhandler(400)
def bad_request(error):
   return render_template('errors/400.html')

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html')

if __name__ == "__main__" :
    app.run()
