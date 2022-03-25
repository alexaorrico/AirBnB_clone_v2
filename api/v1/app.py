#!/usr/bin/python3

"""setting up api functions"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """calls storage.close on teardown"""
    storage.close()

if "HBNB_API_HOST" in os.environ:
    host = os.getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if "HBNB_API_PORT" in os.environ:
    port = os.getenv("HBNB_API_PORT")
else:
    port = 5000

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
