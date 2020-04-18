import functools
try:
    from libmorphing.morphing import ImageMorph
except ImportError:
    import sys
    sys.path.append('../')
    from lib.libmorphing.morphing import ImageMorph
import os
import uuid

from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, session, url_for
)
from threading import Thread

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def home():
    g.user = 'Andrew'
    return render_template('home.html')


@bp.route('/morph', methods=['POST', 'GET'])
def morph():
    if request.method == 'POST':
        # Ensure that we've actually received both image files
        if 'source_img' not in request.files or request.files['source_img'].filename == '':
            flash('No source image')
            return redirect(request.url)
        if 'target_img' not in request.files or request.files['target_img'].filename == '':
            flash('No target image')
            return redirect(request.url)
        # Ensure that the received files are allowed
        if not allowed_file(request.files['source_img'].filename):
            flash('Source image file type is not allowed')
            return redirect(request.url)
        if not allowed_file(request.files['target_img'].filename):
            flash('Target image file type is not allowed')
            return redirect(request.url)

        # Generate the request ID
        req_id = str(uuid.uuid1())
        current_app.logger.info('Received request [{}]'.format(req_id))

        # Create the working directories for the request
        req_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], req_id)
        res_dir = os.path.join(current_app.config['RESULT_FOLDER'], req_id)
        os.makedirs(req_dir)
        os.makedirs(res_dir)

        # Extract the image files from the request and save them in the upload folder
        source_img = request.files['source_img']
        target_img = request.files['target_img']
        source_img_path = os.path.join(req_dir, 'source_img')
        target_img_path = os.path.join(req_dir, 'target_img')
        source_img.save(source_img_path)
        target_img.save(target_img_path)

        source_points = [[167.0, 227.0], [287.0, 227.0], [86.0, 213.0], [368.0, 222.0], [182.0, 372.0], [271.0, 372.0],
                         [233.0, 306.0], [240.0, 8.0], [227.0, 458.0]]
        target_points = [[162.0, 209.0], [305.0, 209.0], [28.0, 15.0], [450.0, 18.0], [198.0, 346.0], [270.0, 345.0],
                         [238.0, 293.0], [233.0, 59.0], [237.0, 382.0]]

        Thread(target=thread_func, args=(source_img_path, target_img_path, source_points, target_points, res_dir)).start()

        return {'uuid': req_id}

    else:
        # g.user = 'Andrew'
        return render_template('home.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def thread_func(source_img_path, target_img_path, source_points, target_points, output_dir):
    ImageMorph(source_img_path, target_img_path, source_points, target_points, output_dir)
