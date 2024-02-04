#!/usr/bin/python3
"""
Starts a flask application
"""
import os
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from werkzeug.exceptions import NotFound
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r'/api/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exc):
    """
    method that calls storage.close()
    """
    storage.close()


@app.errorhandler(NotFound)
def handle_not_found_error(e):
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app_host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    app_port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=app_host, port=app_port, threaded=True)
