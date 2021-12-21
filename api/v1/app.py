#!/usr/bin/python3
"""Script checking status of API"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Call on storage.close that handles teardowns"""
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    """if host == None:
        host = 0.0.0.0"""
    port = getenv("HBNB_API_PORT")
    """if port == None:
        port = 5000"""
    app.run(host=host, port=port, threaded=True)
