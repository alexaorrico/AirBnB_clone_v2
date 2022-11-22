#!/usr/bin/python3
"""
Instantiates a Flask app.
"""


from flask import Flask

import models
from os import getenv

from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDown(exception):
    """Calls storage.close"""
    models.storage.close()


if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = getenv("HBNB_API_PORT")
    app.run(
        host=getenv('HBNB_API_HOST'),
        port=getenv('HBNB_API_PORT')
    )
