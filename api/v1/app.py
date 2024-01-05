#!/usr/bin/python3
"""Contains code to connect to flask api"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """handle @app.teardown_appcontext"""
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
