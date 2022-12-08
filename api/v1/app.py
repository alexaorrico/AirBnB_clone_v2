#!/usr/bin/python3
"""Our (single) Flask webapp instance"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def handle_notfound(exception):
    status = {
        'error': 'Not found'
    }

    return jsonify(status), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True)
