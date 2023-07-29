#!/usr/bin/python3
"""Start server"""

from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(e):
    """Close db session"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port='5000', threaded=True)
