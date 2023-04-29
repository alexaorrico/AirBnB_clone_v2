#!/usr/bin/python3

"""Flask app"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up(exception=None):
    """ closes current session"""
    storage.close()


if __name__ == "__main__":
    app.run(getenv('HBNB_API_HOST', defaults='0.0.0.0'),
            getenv('HBNB_API_PORT', default=5000),
            threaded=True
            )
