import os
from flask import Flask


def create_app(test_config=None):
    # creating and configuring app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE=os.environ.get('DATABASE'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello Dev'

    from . import db, auth, video
    app.register_blueprint(auth.bp)
    app.register_blueprint(video.bp)
    app.add_url_rule('/', endpoint='index')

    return app
