#!/usr/bin/python3
"""
This script initializes a Flask application and sets up the API routes.
"""


from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from models.state import State
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_route(error):
    "Close the SQLAlchemy Session"
    storage.close()

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
