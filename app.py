''''
    adapted from: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
'''

import os
from flask import Flask, request, redirect, flash, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template


app = Flask(__name__)
Mobility(app)

DATASET_NAME = "recyclenet"
UPLOAD_FOLDER = 'ds/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@mobile_template('{mobile/}upload.html')
def upload_file(template):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template(template)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run()
