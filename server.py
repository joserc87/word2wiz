#!/usr/bin/python3

import os
from flask import render_template, Flask, request, send_from_directory
import json
from subprocess import Popen, PIPE
from word2wiz.word2wiz import word2wiz
from zipfile import ZipFile

UPLOAD_FOLDER = '/tmp/word2wiz'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return True


def secure_filename(filename):
    return filename


def generate_zip(docx):
    """Generates a zip from the docx containing the spell, the wizard
    configuration and the txt, and returns the path to that zip file, together
    with the errors and warnings"""
    # file name without the extension and without the path
    filename = os.path.splitext(os.path.basename(docx))[0]

    # File paths:
    # Folder where everything will be generated
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    # Generate the spell
    spell, report = word2wiz(docx)
    # Compile the spell
    p = Popen(['spell',
               '-pretty-print',
               '-document-types-xml', 'data/documenttypes-zorg.xml',
               '-document-type', 'DOCWIZ'],
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(input=bytes(spell, 'utf-8'))  # [0]
    wizard_configuration = stdout.decode()
    errors = stderr.decode() if stderr else None

    zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.zip')
    with ZipFile(zip_filename, 'w') as myzip:
        myzip.writestr(filename + '.spl', spell)
        myzip.writestr(filename + '.txt', report)
        myzip.writestr(filename + '.xml', wizard_configuration)
        if errors:
            myzip.writestr(filename + '.log', errors)

    # Delete docx
    return zip_filename, errors


@app.route("/")
def index():
    return render_template('index.html')


def error(message=None):
    """Helper method to return a error JSON object"""
    data = {"status": "error"}
    if message:
        data["message"] = message
    return json.dumps(data)


def success(file_path, message=None):
    data = {"status": "success",
            "file": file_path}
    if message:
        data["message"] = message
    return json.dumps(data)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upl' not in request.files:
            return error("No file part")
        file = request.files['upl']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return error("No selected file")
        # If the folder does not exist, create it
        if not os.path.isdir(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                xmlfilepath, errors = generate_zip(filepath)
                complete_path = 'uploads/' + os.path.basename(xmlfilepath)
                return success(complete_path, errors)
            except Exception as err:
                return error("Error while parsing the document file\n\n{0}"
                             .format(err))

    return error()


@app.route('/uploads/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename,
                               as_attachment=True,
                               mimetype='application/xml')


if __name__ == "__main__":
    app.run()
