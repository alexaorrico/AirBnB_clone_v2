#!/usr/bin/python3
"""starts a Flask web api"""

from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return make_response({"error": "Not found"}, 404)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
