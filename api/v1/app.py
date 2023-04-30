#!/usr/bin/python3
"""
creating an api
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

api_host = getenv("HBNB_API_HOST", "0.0.0.0")
api_port = getenv("HBNB_API_PORT", 5000)


@app.teardown_appcontext
def close_db(obj):
    """Deletes/removes instance of a session when done with it"""
    storage.close()


if __name__ == "__main__":
    app.run(host=api_host, port=int(api_port), threaded=True)
