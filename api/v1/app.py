#!/usr/bin/python3
"""Start server"""

from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(e):
    """Close db session"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') | '0.0.0.0'
    port = getenv('HBNB_API_PORT') | '5000'
    app.run(host=host, port='5000')
