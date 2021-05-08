#!/usr/bin/python3
"""API steveeeeeeen hola"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_appcontext(stiven):
    """teardown function"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, debug=True, threaded=True)
