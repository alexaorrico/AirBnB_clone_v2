#!/usr/bin/python3
"""Flask app file v1"""

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url="/app_views")

@app.teardown_appcontext
def teardown(exception):
    """calls storage.close"""
    storage.close()


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(
        host=host,
        port=port,
        threaded=True)
