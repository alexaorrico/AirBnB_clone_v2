#!/usr/bin/python3
"""Flask app to hight level structures"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resourses={r"/*": {"origin": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(self):
    """teardown close"""
    storage.close()


@app.errorhandler(404)
def errorhandler404(error):
    """status 404 error handler"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'),
            threaded=True, debug=True)
