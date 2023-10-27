#!/usr/bin/python3
"""Create instance of Flask"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import make_response
from flask import jsonify
from flask_cors import CORS
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(db):
    """This method closes the session"""
    storage.close()


@app.errorhandler(404)
def oops_not_found(error):
    """Handles 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    hst = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    prt = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hst, port=prt, threaded=True)
