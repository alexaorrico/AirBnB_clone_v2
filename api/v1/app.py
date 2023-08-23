#!/usr/bin/python3
""" flusk app """

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(e):
    """ teardown for app """
    storage.close()


if __name__ == "__main__":
    """ ran the app """
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'), threaded=True)
