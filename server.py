#!/usr/bin/python3

import os
from flask import render_template, Flask, request, send_from_directory
from subprocess import Popen, PIPE
from word2wiz.word2wiz import word2wiz
from zipfile import ZipFile

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return True


def secure_filename(filename):
    return filename


def generate_zip(docx):
    """Generates a zip from the docx containing the spell, the wizard
    configuration and the txt, and returns the path to that zip file."""
    # file name without the extension and without the path
    filename = os.path.splitext(os.path.basename(docx))[0]

    # File paths:
    # Folder where everything will be generated
    conversion_folder = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Spell
    os.path.join(conversion_folder, '{0}.spl'.format(filename))
    # Spell
    os.path.join(conversion_folder, '{0}.spl'.format(filename))
    # Generate the spell
    spell, report = word2wiz(docx)
    # Compile the spell
    p = Popen(['spell',
               '-pretty-print',
               '-document-types-xml', 'data/documenttypes-zorg.xml',
               '-document-type', 'DOCWIZ'],
              stdin=PIPE, stdout=PIPE)
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
    return zip_filename


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
            xmlfilepath = generate_zip(filepath)
            return '{"status": "success", "file": "uploads/' + \
                os.path.basename(xmlfilepath) + '"}'
    return '{"status": "error"}'


@app.route('/uploads/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename,
                               as_attachment=True,
                               mimetype='application/xml')

if __name__ == "__main__":
    app.run()
