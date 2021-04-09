from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import sim

app = Flask(__name__)
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/election_sim", methods = ['GET'])
def election_app():
    return render_template("election_sim.html")

@app.route('/election_sim/submission', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'uploads', fname))
        sim.doAllSystems('Simulation', 'instance/uploads/' + fname, sim.NUM, False)
        os.remove(os.path.join(app.instance_path, 'uploads', fname))
        return render_template(
            "submission.html", filename = fname
        )

@app.errorhandler(404)
def page_not_found(error):
   return render_template('errors/404.html'),404

@app.errorhandler(400)
def bad_request(error):
   return render_template('errors/400.html'),400

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'),500

if __name__ == "__main__" :
    app.run()
