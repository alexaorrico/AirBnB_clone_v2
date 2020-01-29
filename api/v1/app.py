#!/usr/bin/python3
"""
 Start Flask Application
"""
from models import storage
from flask import Flask, Blueprint, make_response, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def finish(NaN):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
