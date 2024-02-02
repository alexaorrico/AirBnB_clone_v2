#!/usr/bin/python3
"""Module with a falsk script"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """Module that closes storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Method that returns status 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    import os
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
