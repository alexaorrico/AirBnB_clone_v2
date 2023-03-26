#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
a = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(self):
    """Tear down"""
    storage.close()


@app.errorhandler(404)
def notfound(e):
    """Error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST"), port=getenv("HBNB_API_PORT"),
            threaded=True)
