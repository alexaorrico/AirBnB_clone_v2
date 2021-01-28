#!/usr/bin/python3
"""Our first API"""


from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
# blueprint is registered to the app


@app.teardown_appcontext
def teardown(error):
    """Method that handles teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(e):
    """ returns a JSON-formatted
    404 status code response
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host=os.getenv("HBNB_API_HOST"),
            port=os.getenv("HBNB_API_PORT"), threaded=True)
