#!/usr/bin/python3
""" app.py """


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST"),
            port=os.getenv("HBNB_API_PORT"), threaded=True)
