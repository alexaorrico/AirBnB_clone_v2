#!/usr/bin/python3
""" app.py """


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST"),
            port=os.getenv("HBNB_API_PORT"), threaded=True)
