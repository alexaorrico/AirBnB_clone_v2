#!/usr/bin/python3
"""Task 0"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import make_response
from flask import jsonify
import os


app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_session(db):
    """This method allow close the session"""
    storage.close()


if __name__ == "__main__":
    hst = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    prt = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hst, port=prt, threaded=True)
