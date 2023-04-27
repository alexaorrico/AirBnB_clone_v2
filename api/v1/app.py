#!/usr/bin/python3
""" Flask Application """

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, render_template, make_response, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """ Close Storage """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')))
