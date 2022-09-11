#!/usr/bin/python3
"""Create a variable app, instance of Flask"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """function teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """Function that handles error 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.route('/', methods=['GET'])
def get_post():
    return jsonify


if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
