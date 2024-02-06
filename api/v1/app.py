#!/usr/bin/python3
""" flask app set up"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
import os

app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def db_close(exception=None):
    """ close db session after each request"""

    storage.close()


@app.errorhandler(404)
def error_page(e):
    """ error page"""

    obj = {"error": "Not found"}
    return jsonify(obj), 404


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
