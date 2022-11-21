#!/usr/bin/python3
"""
Instantiates a Flask app.
"""


from flask import Flask

import models
from os import getenv

from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def tearDown(exception):
    """Calls storage.close"""
    models.storage.close()


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST'),
        port=getenv('HBNB_API_PORT')
    )
