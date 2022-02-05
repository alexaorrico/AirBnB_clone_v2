#!/usr/bin/python3
"""
Create an api
"""

from os import getenv
from api.v1.views import app_views
from models import storage
from flask import Flask

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Close session """
    storage.close()


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
