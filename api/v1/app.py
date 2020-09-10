#!/usr/bin/python3
"""init flask"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_close(db_close):
    """close the ssesion"""
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    """return error 404"""
    return jsonify({
                    "error": "Not found" 
                  }), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.url_map.strict_slashes = False
    app.run(host, port, threaded=True)
