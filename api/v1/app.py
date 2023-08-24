#!/usr/bin/python3
"""
Server file for HBNB version 3
"""
from flask import Flask
from models import storage
import os
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == "__main__":
    hoster = os.getenv('HBNB_API_HOST', '0.0.0.0')
    porter = os.getenv('HBNB_API_PORT', '5000')

    app.run(host=hoster, port=porter, threaded=True)
