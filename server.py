#!/usr/bin/python

import os
from flask import render_template, Flask, request, send_from_directory
from subprocess import Popen, PIPE
from word2wiz import word2wiz

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return True

def secure_filename(filename):
    return filename

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upl' not in request.files:
            flash('No file part')
            return '{"status": "error"}'
        file = request.files['upl']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return '{"status": "error"}'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            spell = word2wiz(filepath)
            xmlfilepath = filepath + '.xml'
            p = Popen(['spell', '-pretty-print', '-o', xmlfilepath],
                      stdin=PIPE, stdout=PIPE)
            stdout = p.communicate(input=bytes(spell, 'utf-8'))[0]
            print(stdout.decode())
            return '{"status": "success", "file": "' + xmlfilepath + '"}'
    return '{"status": "error"}'

@app.route('/uploads/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename,
                               as_attachment=True,
                               mimetype='application/xml')

if __name__ == "__main__":
    app.run()
