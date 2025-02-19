#!/usr/bin/python3
"""App module"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Teardown function"""
    storage.close()


@app.errorhandler(404)
def error_404(e):
    """Page not found"""
    err = {"error": "Not found"}
    return err, 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
