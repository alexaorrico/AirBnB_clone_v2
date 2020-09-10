#!/usr/bin/python3
"""first endpoint (route)"""
from models import storage
from flask import Flask, jsonify, make_response
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
host = getenv("HBNB_API_HOST") or '0.0.0.0'
port = getenv("HBNB_API_PORT") or 5000


@app.teardown_appcontext
def teardown(self):
    """teardown close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handler error 404 """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
