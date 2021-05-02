#imports
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from os import path, makedirs, getenv, remove
from glob import glob
from json import dumps
from sim import processData, doAllSystems, NUM, IMGFILEFORMAT

#setup
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024
app.secret_key = getenv("SECRET_KEY")
UPLOAD_FOLDER = 'uploads'
UPLOAD_FILEROOT = 'userUpload'
UPLOAD_FILEEXT = '.txt'
EXT_INDEX = -(len(UPLOAD_FILEEXT))
UPLOAD_RESULT = 'results'
UPLOAD_IMAGES = 'img'
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

@app.route("/temp_app", methods = ['GET'])
def temp_app():
    return render_template("temp_app.html")

@app.route('/election_sim/file_submit', methods = ['POST'])
def upload_file():
    f = request.files['file']
    fname = secure_filename(f.filename)
    if fname.endswith(UPLOAD_FILEEXT):
        wholeFilename = PATH_STRING + fname
        f.save(wholeFilename)
        makedirs(PATH_STRING + fname[:EXT_INDEX] + UPLOAD_IMAGES, exist_ok=True)
        return dumps(processData(wholeFilename, fname[:EXT_INDEX]))
    return render_template("election_sim.html")

@app.route('/election_sim/text_submit', methods = ['POST'])
def upload_text():
    text = request.form['text']
    newRoot = newUploadFileRoot()
    wholeFilename = PATH_STRING + newRoot + UPLOAD_FILEEXT
    with open(wholeFilename, 'w') as f:
        f.write(text)
    makedirs(PATH_STRING + newRoot + UPLOAD_IMAGES, exist_ok=True)
    return dumps(processData(wholeFilename, newRoot))

@app.route('/election_sim/run_file/<filename>', methods = ['GET'])
def run_file(filename):
    filepath = nameToPath(filename)
    imgfilepath = path.join(filepath[:EXT_INDEX] + UPLOAD_IMAGES, '')
    if path.isfile(filepath):
        resultString = doAllSystems('Simulation',  filepath, imgfilepath, NUM, False)
        with open(PATH_STRING + filename[:EXT_INDEX] + UPLOAD_RESULT + UPLOAD_FILEEXT, 'w') as f:
            f.write(resultString)
        num = str(len(glob(imgfilepath + '*')))
        obj = {
            "textResult": resultString,
            "numFiles": num,
            "imgFolderName": filename[:EXT_INDEX] + UPLOAD_IMAGES
        }
        return dumps(obj)
    return render_template("election_sim.html")

@app.route('/election_sim/download_file/<filename>', methods = ['GET'])
def download_file(filename):
    filepath = nameToPath(filename)
    if path.isfile(filepath):
        return send_file(filepath, as_attachment=True, cache_timeout=0)

@app.route('/election_sim/img/<folder>/<filename>', methods = ['GET'])
def get_img(folder, filename):
    filepath = path.join(PATH_STRING + folder, filename)
    if path.isfile(filepath):
        return send_file(filepath, mimetype='image/png')

@app.route('/election_sim/delete_file/<filename>', methods = ['DELETE'])
def delete_file(filename):
    filepath = nameToPath(filename)
    if path.exists(filepath):
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