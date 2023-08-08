#!/usr/bin/python3
""" Module containing Flask application """
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ closes the storage """
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """ Returns a JSON formatted 404 status code response """
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    if host is None:
        host = '0.0.0.0'
    port = getenv("HBNB_API_PORT")
    if port is None:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
