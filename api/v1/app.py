#!/usr/bin/python3
"""
Create a api
"""


from os import getenv
from api.v1.views import app_views
from models import storage
from flask import Flask, Blueprint
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    """if getenv(HBNB_API_HOST) or getenv(HBNB_API_PORT):
        host = getenv(HBNB_API_HOST)
        port = getenv(HBNB_API_PORT)
    else:
        host = '0.0.0.0'
        port = 5000"""

    app.run(host='0.0.0.0', port=5000, threaded=True)
