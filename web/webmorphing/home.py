import functools
import os

from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, session, url_for
)
#from werkzeug.security import check_password_hash, generate_password_hash
# from flask_uploads import UploadSet, IMAGES
from werkzeug.utils import secure_filename


#from flaskr.db import get_db


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def home():
    g.user = 'Andrew'
    return render_template('home.html')


# @bp.route('/upload', methods=['POST'])
# def upload_file():
#     print('Hello, upload')
#     # Check if the post request has the file part
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     # If user does not select file, browser also submit an empty part without filename
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
#         # return redirect(url_for('uploaded_file', filename=filename))

# photos = UploadSet('photos', IMAGES)


@bp.route('/morph', methods=['POST', 'GET'])
def morph():
    if request.method == 'POST':
        print('Hello, upload')
        print(request.files)
        if 'source_img' not in request.files or request.files['source_img'].filename == '':
            flash('No source image')
            return redirect(request.url)
        if 'target_img' not in request.files or request.files['target_img'].filename == '':
            flash('No target image')
            return redirect(request.url)

        source_img = request.files['source_img']
        target_img = request.files['target_img']

        source_img_filename = secure_filename(source_img.filename)
        target_img_filename = secure_filename(target_img.filename)

        print('source image: ' + source_img_filename)
        print('target image: ' + target_img_filename)

        source_img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], source_img_filename))
        target_img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], target_img_filename))

        # rec = Photo(filename=filename, user=g.user.id)
        # rec.store()
        flash("Photo saved.")
        # return redirect(url_for('show', id=rec.id))


        # Check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # If user does not select file, browser also submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        #     # return redirect(url_for('uploaded_file', filename=filename))
    else:
        g.user = 'Andrew'
        return render_template('home.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
