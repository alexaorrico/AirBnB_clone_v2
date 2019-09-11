#!/usr/bin/python3

""" app file
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


h = os.environ.get("HBNB_API_HOST", "0.0.0.0")
p = os.environ.get("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def close(exception=None):
    storage.close()

if __name__ == "__main__":
    app.run(host=str(h), port=int(p), threaded=True, debug=True)
