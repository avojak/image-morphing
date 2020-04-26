try:
    from libmorphing.morphing import ImageMorph
except ImportError:
    import sys

    sys.path.append('../')
    from lib.libmorphing.morphing import ImageMorph
import base64
import cv2
import io
import json
import os
import uuid
import validators

from flask import (
    abort, Blueprint, flash, g, current_app, redirect, render_template, request, url_for, jsonify)
from threading import Thread

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@bp.route('/morph', methods=['POST', 'GET'])
def morph():
    if request.method == 'POST':
        # Ensure that we've actually received both image files
        if 'source-img' not in request.files or request.files['source-img'].filename == '':
            flash('No source image.')
            return redirect(request.url)
        if 'target-img' not in request.files or request.files['target-img'].filename == '':
            flash('No target image.')
            return redirect(request.url)

        # Ensure that the received files are allowed
        if not allowed_file(request.files['source-img'].filename):
            flash('Source image file type is not allowed.')
            return redirect(request.url)
        if not allowed_file(request.files['target-img'].filename):
            flash('Target image file type is not allowed.')
            return redirect(request.url)

        # Ensure that we've received the source and target points
        source_points = json.loads(request.form['source_points'])
        target_points = json.loads(request.form['target_points'])
        if len(source_points) == 0:
            flash('No source points selected.')
            return redirect(request.url)
        if len(target_points) == 0:
            flash('No target points selected.')
            return redirect(request.url)

        # Ensure that we've received the GIF duration and FPS
        gif_duration = json.loads(request.form['gif_duration'])
        gif_fps = json.loads(request.form['gif_fps'])
        if gif_duration == '':
            flash('No GIF duration provided.')
            return redirect(request.url)
        if gif_fps == '':
            flash('No GIF FPS provided.')
            return redirect(request.url)

        # Generate the request ID
        req_id = str(uuid.uuid1())
        current_app.logger.info('Received request [{}]'.format(req_id))

        # Create the working directories for the request
        req_dir = get_req_dir(req_id)
        res_dir = get_res_dir(req_id)
        os.makedirs(req_dir)
        os.makedirs(res_dir)

        # Extract the image files from the request and save them in the upload folder
        source_img = request.files['source-img']
        target_img = request.files['target-img']
        source_img_path = os.path.join(req_dir, 'source_img')
        target_img_path = os.path.join(req_dir, 'target_img')
        source_img.save(source_img_path)
        target_img.save(target_img_path)

        # Verify image dimensions
        source_shape = cv2.imread(source_img_path).shape
        target_shape = cv2.imread(target_img_path).shape
        if source_shape[0] > 600 or source_shape[1] > 600 or target_shape[0] > 600 or target_shape[1] > 600:
            flash('Maximum image resolution is 600x600.')
            return redirect(request.url)
        if source_shape != target_shape:
            flash('Source and target image have mismatching resolutions.')
            return redirect(request.url)

        Thread(target=thread_func,
               args=(source_img_path, target_img_path, source_points, target_points, res_dir, gif_duration, gif_fps)
               ).start()

        return redirect(url_for('home.morph_result', req_id=req_id))
    else:
        return render_template('home.html')


@bp.errorhandler(413)
def page_not_found(e):
    flash('Request entity too large.')
    return render_template('home.html'), 200


@bp.route('/morph/<req_id>', methods=['GET'])
def morph_result(req_id):
    validate_request_id(req_id)
    g.req_id = req_id
    return render_template('results.html')


@bp.route('/results/<req_id>/source-image', methods=['GET'])
def get_source_image(req_id):
    validate_request_id(req_id)
    return get_image(os.path.join(get_req_dir(req_id), 'source_img'))


@bp.route('/results/<req_id>/target-image', methods=['GET'])
def get_target_image(req_id):
    validate_request_id(req_id)
    return get_image(os.path.join(get_req_dir(req_id), 'target_img'))


@bp.route('/results/<req_id>/point-mapping-image', methods=['GET'])
def get_point_mapping_image(req_id):
    validate_request_id(req_id)
    return get_image(os.path.join(get_res_dir(req_id), 'mapping.png'))


@bp.route('/results/<req_id>/source-triangulation-image', methods=['GET'])
def get_source_triangulation_image(req_id):
    validate_request_id(req_id)
    return get_image(os.path.join(get_res_dir(req_id), 'source_triangulation.png'))


@bp.route('/results/<req_id>/target-triangulation-image', methods=['GET'])
def get_target_triangulation_image(req_id):
    validate_request_id(req_id)
    return get_image(os.path.join(get_res_dir(req_id), 'target_triangulation.png'))


@bp.route('/results/<req_id>/morphing-gif', methods=['GET'])
def get_morphing_gif(req_id):
    validate_request_id(req_id)
    return get_image(os.path.join(get_res_dir(req_id), 'morphing.gif'))


def validate_request_id(req_id):
    if not validators.uuid(req_id):
        abort(400)


def get_image(img_path):
    if os.path.exists(img_path) and os.path.isfile(img_path):
        with open(img_path, 'rb') as img_file:
            output = io.BytesIO()
            output.write(img_file.read())
            output.seek(0)
            img_base64 = base64.b64encode(output.read())
            return jsonify({'data': str(img_base64)})
    else:
        return jsonify({'data': ''})


def get_req_dir(req_id):
    return os.path.join(current_app.config['UPLOAD_FOLDER'], req_id)


def get_res_dir(req_id):
    return os.path.join(current_app.config['RESULT_FOLDER'], req_id)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def thread_func(source_img_path, target_img_path, source_points, target_points, output_dir, gif_duration, gif_fps):
    ImageMorph(source_img_path, target_img_path, source_points, target_points, output_dir, gif_duration, gif_fps)
