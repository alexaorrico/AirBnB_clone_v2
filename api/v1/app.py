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

if getenv('HBNB_API_HOST') is none:
    host = 0.0.0.0
else:
    host = 'HBNB_API_HOST'

if getenv('HBNB_API_PORT') is none:
    port = 5000
else:
    port = 'HBNB_API_PORT'

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    return storage.close()

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host=host, port=port)
