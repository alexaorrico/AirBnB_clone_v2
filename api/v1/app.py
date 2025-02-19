#!/usr/bin/python3
""" """
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, abort
from flask import render_template, jsonify
from flask import make_response
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
""" CORS for Task 12 """
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def invalid_route(e):
    """ 404 for Task 5? """
    return (jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def storage_close(issue):
    """ declare a method ...calls storage.close() """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')),
            threaded=True, debug=True)
