#!/usr/bin/python3
""" main app.py """
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(ex):
    """ tear down """
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')
    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True)
