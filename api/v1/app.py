#!/usr/bin/python3
"""creates an instance of Flask"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardowndb(exception):
    """close storage"""
    storage.close()


def start_flask():
    """start flask"""
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)

if __name__ == "__main__":
    start_flask()
