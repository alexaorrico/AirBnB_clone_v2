#!/usr/bin/python3
""" Root of application """
from os import getenv
from flask import Flask, make_response, jsonify
from .views import app_views
from models import storage

# globals
HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')


def create_app(config_name):
    ''' Main func, avoid litter global space'''
    app = Flask(__name__)
    # set configs if available
    if config_name is not None:
        app.config.from_object(config_name)
    # register blueprints
    app.register_blueprint(app_views)

    # normally do this in another file then import here but pep8
    @app.teardown_appcontext
    def teardown(self):
        ''' Close session '''
        storage.close()

    @app.errorhandler(404)
    def not_found(e):
        """Error handler for the application"""
        return make_response(jsonify({'error': 'Not found'}), 404)

    return app


if __name__ == "__main__":
    """Start of application"""
    app = create_app(None)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
