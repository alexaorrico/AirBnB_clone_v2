#!/usr/bin/python3
"""Start Api."""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection after each request."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error handler."""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=getenv("HBNB_API_PORT", "5000"),
        threaded=True,
    )
