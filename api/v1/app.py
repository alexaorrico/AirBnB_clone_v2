#!/usr/bin/python3

"""flask app file module"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_storage(exception):
    """method handles close storage"""
    storage.close()


@app.errorhandler(404)
def nop_404(err):
    """
    For handling the 404 error page
    """
    j_404 = {
        "error": "Not found"
    }
    return jsonify(j_404), 404


@app.errorhandler(400)
def resource_not_found(e):
    j_400 = {
        "error": "Bad Request",
        "message": str(e.description) if e.description else "Not a JSON"
    }
    return jsonify(j_400), 400


if __name__ == "__main__":
    """Run and excute the flask api on all ip port 5000"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, debug=True, threaded=True)
