#imports
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from os import path, makedirs, getenv, remove
from glob import escape, glob
from json import dumps
from sim import processData, doAllSystems, NUM

#setup
UPLOAD_FOLDER = 'uploads'
UPLOAD_FILENAME = 'userUpload.txt'
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.secret_key = getenv("SECRET_KEY")
makedirs(path.join(app.instance_path, UPLOAD_FOLDER), exist_ok=True)

#helper functions
def fileUploaded(ps):
    return (len(glob(ps + '*')) != 0)

def pathString():
    return escape(path.join(app.instance_path, UPLOAD_FOLDER, ''))

def uploadedFilename(ps):
    return glob(ps + '*')[0];

#routes
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/election_sim", methods = ['GET'])
def election_app():
    return render_template("election_sim.html")

@app.route('/election_sim/file_submit', methods = ['POST'])
def upload_file():
    if not fileUploaded(pathString()):
        f = request.files['file']
        fname = secure_filename(f.filename)
        wholeFilename = path.join(app.instance_path, UPLOAD_FOLDER, fname)
        if '.txt' in fname:
            f.save(wholeFilename)
            return dumps(processData(wholeFilename))
    return render_template("election_sim.html")

@app.route('/election_sim/text_submit', methods = ['POST'])
def upload_text():
    if not fileUploaded(pathString()):
        text = request.form['text']
        wholeFilename = path.join(app.instance_path, UPLOAD_FOLDER, UPLOAD_FILENAME)
        with open(wholeFilename, 'w') as f:
            f.write(text)
        return dumps(processData(wholeFilename))
    return render_template("election_sim.html")

@app.route('/election_sim/run_file', methods = ['GET'])
def run_file():
    ps = pathString()
    if fileUploaded(ps):
        resultString = doAllSystems('Simulation', uploadedFilename(ps), NUM, False)
        remove(uploadedFilename(ps))
        return resultString
    return render_template("election_sim.html")

@app.route('/election_sim/download_file', methods = ['GET'])
def download_file():
    ps = pathString()
    if fileUploaded(ps):
        return send_file(uploadedFilename(ps), as_attachment=True)
    return render_template("election_sim.html")

@app.route('/election_sim/delete_file', methods = ['DELETE'])
def delete_file():
    ps = pathString()
    if fileUploaded(ps):
        remove(uploadedFilename(ps))
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