#!/usr/bin/pyhton3
"""
flask application
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def toclose(exception):
    """
    Handle app.teardown and calls close function
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a JSON-formatted
    404 status code response"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    app.run(host, port, threaded=True)
