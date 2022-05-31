#!/usr/bin/python3
"""
Your first endpoint (route) will be to return the status of your API
"""
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
swagger_template = {
    'swagger': '2.0',
    'info': {
        'title': 'HBNB',
        'description': 'RESTFul API for HBNB',
        'version': '1.0.0'
    },
}
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
swagger = Swagger(app, template=swagger_template)


@app.teardown_appcontext
def close(self):
    """ Close storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', 5000)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
