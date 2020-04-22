import functools
try:
    from libmorphing.morphing import ImageMorph
except ImportError:
    import sys
    sys.path.append('../')
    from lib.libmorphing.morphing import ImageMorph
import base64
import io
import os
import uuid
import validators

from flask import (
    abort, Blueprint, flash, g, current_app, redirect, render_template, request, session, url_for,
    send_file, make_response, jsonify)
from threading import Thread
from urllib.parse import quote

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def home():
    g.user = 'Andrew'
    return render_template('home.html')


@bp.route('/morph', methods=['POST', 'GET'])
def morph():
    if request.method == 'POST':
        print(request.files)
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
        req_dir = get_req_dir(req_id)
        res_dir = get_res_dir(req_id)
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

        # g.req_id = req_id
        return redirect(url_for('home.morph_result', req_id=req_id))
    else:
        # if 'req_id' in request.args.keys():
        #     g.req_id = request.args.get('req_id')
        #     return render_template('results.html')
        # else:
        # g.user = 'Andrew'
        return render_template('home.html')


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


def thread_func(source_img_path, target_img_path, source_points, target_points, output_dir):
    ImageMorph(source_img_path, target_img_path, source_points, target_points, output_dir)
