#!/usr/bin/python3
""" API Status Application Instance Module """
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(exception):
    """handles 404 error"""
    not_found_error = {"error": "Not found"}
    return jsonify(not_found_error)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"

    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    else:
        port = "5000"

    app.run(host=host, port=port, threaded=True)
