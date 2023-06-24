#!/usr/bin/python3
"""It’s time to start your API!."""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_db(exception):
    """
    Is function "close_db" takes an error as input and does not have any\
    code implemented within it.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Is description: a resource was not found.
    """
    return jsonify({'error': "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
