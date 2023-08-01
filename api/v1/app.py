#!/usr/bin/python3

"""
This is Flask App
We are setting this up to manage  other blueprints
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_404(error):
    """handles resource not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_storage(exeception):
    """calls storage.close()"""
    storage.close()


if __name__ == '__main__':
    host_to_use = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port_to_use = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host_to_use, port=port_to_use, threaded=True, debug=True)
