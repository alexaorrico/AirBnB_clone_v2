#!/usr/bin/python3
"""Create instance of flask"""
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


@app.errorhandler(404)
def not_found(error):
    """ Handler for 404 errors that returns a JSON 404 status code"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_session(db):
    """This method allow close the session"""
    storage.close()


if __name__ == "__main__":
    hst = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    prt = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hst, port=prt, threaded=True)
