#!/usr/bin/python
""" API class """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def _handle_api_error(ex):
    return jsonify(error="Not found")


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=getenv('HBNB_API_PORT') or 5000, threaded=True)
