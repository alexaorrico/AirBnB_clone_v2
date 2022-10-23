#!/usr/bin/python3
""" api module """
from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resourses={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def remove_session(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'),
            threaded=True)
