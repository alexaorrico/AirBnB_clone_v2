#!/usr/bin/python3
"""creates an instance of a flask app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(os.getenv("HBNB_API_PORT", default=5000)),
            threaded=True)
