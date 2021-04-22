#imports
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from os import path, makedirs, getenv, remove
from glob import glob
from json import dumps
from sim import processData, doAllSystems, NUM

#setup
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024
app.secret_key = getenv("SECRET_KEY")
UPLOAD_FOLDER = 'uploads'
UPLOAD_FILEROOT = 'userUpload'
UPLOAD_FILEEXT = '.txt'
EXT_INDEX = -(len(UPLOAD_FILEEXT))
UPLOAD_RESULT = 'results'
PATH_NAME = path.join(app.instance_path, UPLOAD_FOLDER)
PATH_STRING = path.join(PATH_NAME, '')
makedirs(PATH_NAME, exist_ok=True)

#helper functions
def newUploadFileRoot():
    return UPLOAD_FILEROOT + str(len(glob(PATH_STRING + '*')))

def nameToPath(filename):
    return PATH_STRING + secure_filename(filename)

#routes
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/election_sim", methods = ['GET'])
def election_app():
    return render_template("election_sim.html")

@app.route('/election_sim/file_submit', methods = ['POST'])
def upload_file():
    f = request.files['file']
    fname = secure_filename(f.filename)
    if fname.endswith(UPLOAD_FILEEXT):
        wholeFilename = PATH_STRING + fname
        f.save(wholeFilename)
        return dumps(processData(wholeFilename, fname[:EXT_INDEX]))
    return render_template("election_sim.html")

@app.route('/election_sim/text_submit', methods = ['POST'])
def upload_text():
    text = request.form['text']
    wholeFilename = PATH_STRING + newUploadFileRoot() + UPLOAD_FILEEXT
    with open(wholeFilename, 'w') as f:
        f.write(text)
    return dumps(processData(wholeFilename, newUploadFileRoot()))

@app.route('/election_sim/run_file/<filename>', methods = ['GET'])
def run_file(filename):
    filepath = nameToPath(filename)
    if path.isfile(filepath):
        resultString = doAllSystems('Simulation',  filepath, NUM, False)
        with open(PATH_STRING + filename[:EXT_INDEX] + UPLOAD_RESULT + UPLOAD_FILEEXT, 'w') as f:
            f.write(resultString)
        #remove(filepath)
        return resultString
    return render_template("election_sim.html")

@app.route('/election_sim/download_file/<filename>', methods = ['GET'])
def download_file(filename):
    filepath = nameToPath(filename)
    if path.isfile(filepath):
        return send_file(filepath, as_attachment=True, cache_timeout=0)

@app.route('/election_sim/delete_file/<filename>', methods = ['DELETE'])
def delete_file(filename):
    filepath = nameToPath(filename)
    if path.isfile(filepath):
        remove(filepath)
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