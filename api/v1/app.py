#!/usr/bin/python3
"""
    Flask App that integrates the  API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import *


app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown(excep):
    """
        close sqlAlch session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port)
