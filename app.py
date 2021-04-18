#imports
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import glob
import sim

#setup
app = Flask(__name__)
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)

#routes
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/election_sim", methods = ['GET'])
def election_app():
    return render_template("election_sim.html")

@app.route('/election_sim/file_submit', methods = ['POST'])
def upload_file():
    pathString = glob.escape(os.path.join(app.instance_path, 'uploads', ''))
    fileUploaded = (len(glob.glob(pathString + '*')) != 0)
    if request.method == 'POST' and not fileUploaded:
        f = request.files['file']
        fname = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'uploads', fname))
    return render_template("election_sim.html")
    #     sim.doAllSystems('Simulation', 'instance/uploads/' + fname, sim.NUM, False)
    #     os.remove(os.path.join(app.instance_path, 'uploads', fname))
    # return render_template("submission.html", filename = fname)

@app.route('/election_sim/text_submit', methods = ['POST'])
def upload_text():
    pathString = glob.escape(os.path.join(app.instance_path, 'uploads', ''))
    fileUploaded = (len(glob.glob(pathString + '*')) != 0)
    if request.method == 'POST' and not fileUploaded:
        text = request.form['text']
        with open(os.path.join(app.instance_path, 'uploads', 'userUpload.txt'), 'w') as f:
            f.write(text)
    return render_template("election_sim.html")

@app.route('election_sim/process_file', methods = ['GET'])
def pull_data():
    pathString = glob.escape(os.path.join(app.instance_path, 'uploads', ''))
    fileUploaded = (len(glob.glob(pathString + '*')) != 0)
    if request.method == 'GET' and fileUploaded:
        return sim.processData(glob.glob(pathString + '*')[0])
    return render_template("election_sim.html")

#error handlers
@app.errorhandler(404)
def page_not_found(error):
   return render_template('errors/404.html'),404

@app.errorhandler(400)
def bad_request(error):
   return render_template('errors/400.html'),400

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'),500

#this thing
if __name__ == "__main__" :
    app.run()