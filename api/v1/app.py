#!/usr/bin/python3

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    teardown_appcontext closes the Session Object
    """
    storage.close()


@app.errorhandler(404)
def not_found_error(message):
    """
    404 error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':

    app.run(host=host,
            port=port,
            threaded=True)
