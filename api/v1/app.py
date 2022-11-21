#!/usr/bin/python3
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv 

app = Flask(__name__)


app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(tear):
    """closes the storage engine"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ a handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404



if __name__ == "__main__":
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
