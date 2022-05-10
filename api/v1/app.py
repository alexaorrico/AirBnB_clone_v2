#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    storage.close()


if __name__ == "__main__":
    h = os.getenv("HBNB_API_HOST") or "0.0.0.0"
    p = os.getenv("HBNB_API_PORT") or 5000
    app.run(host=h, port=p, threaded=True)
