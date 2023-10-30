#!/usr/bin/python3
"""
API
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
# host = getenv("HBNB_API_HOST")
# port = getenv("HBNB_API_PORT")


@app.teardown_appcontext
def teardown(err):
    """teardown content"""
    from models import storage

    storage.close()


@app.errorhandler(404)
def error404(err):
    """Return a custom 404 page"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # host = host if host else "0.0.0.0"
    # port = port if port else "5000"
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
