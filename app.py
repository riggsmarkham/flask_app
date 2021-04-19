#imports
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from os import path, makedirs, getenv
from glob import escape, glob
from json import dumps
import sim

#setup
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.secret_key = getenv("SECRET_KEY")
makedirs(path.join(app.instance_path, 'uploads'), exist_ok=True)

#routes
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/election_sim", methods = ['GET'])
def election_app():
    return render_template("election_sim.html")

@app.route('/election_sim/file_submit', methods = ['POST'])
def upload_file():
    pathString = escape(path.join(app.instance_path, 'uploads', ''))
    fileUploaded = (len(glob(pathString + '*')) != 0)
    if not fileUploaded:
        f = request.files['file']
        fname = secure_filename(f.filename)
        if '.txt' in fname:
            f.save(path.join(app.instance_path, 'uploads', fname))
    return render_template("election_sim.html")

@app.route('/election_sim/text_submit', methods = ['POST'])
def upload_text():
    pathString = escape(path.join(app.instance_path, 'uploads', ''))
    fileUploaded = (len(glob(pathString + '*')) != 0)
    if not fileUploaded:
        text = request.form['text']
        with open(path.join(app.instance_path, 'uploads', 'userUpload.txt'), 'w') as f:
            f.write(text)
    return render_template("election_sim.html")

@app.route('/election_sim/process_file', methods = ['GET'])
def pull_data():
    pathString = escape(path.join(app.instance_path, 'uploads', ''))
    fileUploaded = (len(glob(pathString + '*')) != 0)
    if fileUploaded:
        return dumps(sim.processData(glob(pathString + '*')[0]))
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