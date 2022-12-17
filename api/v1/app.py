#!/usr/bin/python3
""" connection  """

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Calls storage.close """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Method to handle errors """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """ running conecction """
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True, debug=True)
