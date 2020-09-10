#!/usr/bin/python3
"""
Flask api app file
"""
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """ close session """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ 404 not found """
    return jsonify({"error": "Not found"})

  
if __name__ == "__main__":
    from os import getenv
    host, port = getenv('HBNB_API_HOST'), getenv('HBNB_API_PORT')
    host = "0.0.0.0" if host is None else host
    port = 5000 if port is None else port

    app.run(host=host, port=port, threaded=True)
