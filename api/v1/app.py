#!/usr/bin/python3
"""
Module app
"""
from api.v1.views import app_views
from flask import (Blueprint, Flask, jsonify, Response)
from flask_cors import (CORS, cross_origin)
from models import storage
from os import getenv


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


cors = CORS(app, resources={
            r'/*': {'origins': os.getenv('HBNB_API_HOST', '0.0.0.0')}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """json 404 page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')),
            threaded=True)
