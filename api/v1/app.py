#!/usr/bin/python3
""" App Flask """
from flask_cors import CORS
from os import environ
from models import storage
from flask import Flask, make_response, jsonify
from flasgger import Swagger
from api.v1.views import app_views
from os import getenv

application = Flask(__name__)
application.register_blueprint(app_views)
CORS(application, resources={"/*": {"origins": "0.0.0.0"}})
# Define Swagger configuration
application.config['SWAGGER'] = {
            'title': 'My Awesome API',
            'uiversion': 3,
            'specs': [
                {
                    'version': '1.0',
                    'title': 'My API',
                    'endpoint': 'v1_views',
                    'description': 'A fantastic REST API for various purposes',
                    'route': '/v1/views',
                }
            ]
}
swagger = Swagger(application)


@application.teardown_appcontext
def close_storage(exception):
    """ Closes storage session """
    storage.close()


@application.errorhandler(404)
def handle_404(err):
    """ Returns JSON response with 404 status """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    application.run(host=host, port=port, threaded=True)
