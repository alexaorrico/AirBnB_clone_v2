#!/usr/bin/python3
""" Status of your API """
import os
from flask import Flask, make_response, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def error(exception=None):
    """function to handle error """
    return make_response(jsonify({'error': "Not found"}), 404)


@app.teardown_appcontext
def tearDown(exception=None):
    """ close DB connection session """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True)
