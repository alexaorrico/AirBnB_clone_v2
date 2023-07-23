#!/usr/bin/python3
"""
Starts up a copy of a flask-app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown
def teardown(error):
    storage.close()

if __name__ =="__main__":

    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_HOST", 5000))

    app.run(host=host, port=port, threaded=True)
