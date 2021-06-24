#!/usr/bin/python3
"""
Creates an instances of Flask,
creates Blueprint instance,
and handles teardown
"""

from api.v1.views import app_views
from models import storage
from flask import Flask
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    storage.close()

if __name__ == "__main__":
    app.run(debug=True, threaded=True, 
            host=(getenv('HBNB_API_HOST', '0.0.0.0'))
            port=int(getenv('HBNB_API_PORT', '5000')))
