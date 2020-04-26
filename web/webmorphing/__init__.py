import logging
import os

from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER='/tmp/webmorphing/uploads/',
        RESULT_FOLDER='/tmp/webmorphing/results/',
        ALLOWED_EXTENSIONS=['jpg', 'png', 'jpeg'],
        MAX_CONTENT_LENGTH=(2*1024*1024)  # 2MB
    )

    app.logger.setLevel(logging.INFO)

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure that the upload and result folders exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    from . import home
    app.register_blueprint(home.bp)

    return app
