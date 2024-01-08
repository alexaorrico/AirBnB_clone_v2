#!/usr/bin/python3

"""creating an instance of flask"""

from flask import Flask, jsonify
from models import storage
from api.vi.views import app_views
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
