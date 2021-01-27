#!/usr/bin/python3
"""
Module for hbnb API api
"""
from flask import Flask, render_template, Blueprint, jsonify
from models import storage
import os
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_api(exception):
    """After query return ends current session"""
    return storage.close()


@app.errorhandler(404)
def not_found(self):
    """Handles page not found error"""
    notfound = (jsonify({"error": "Not found"}), 404)
    return notfound


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = int(os.getenv('HBNB_API_PORT'))
    
    #if !host:
    #    os.environ['HBNB_API_HOST'] = '0.0.0.0'
    #    host = os.getenv('HBNB_API_HOST')
    #port = int(os.getenv('HBNB_API_PORT'))
    #if !port:
    #    os.environ['HBNB_API_PORT'] = int(5000)
    #    port = int(os.getenv('HBNB_API_PORT'))

    app.run(host=host, port=port, threaded=True)
