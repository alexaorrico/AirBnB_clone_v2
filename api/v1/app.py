#!/usr/bin/python3
"""
API
"""
from flask import Flask
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")

@app.teardown_appcontext
def teardown(err):
    """teardown content"""
    from models import storage

    storage.close()


if __name__ == "__main__":
    host = host if host else "0.0.0.0"
    port = port if port else "5000"
    app.run(host=host, port=port, threaded=True)
