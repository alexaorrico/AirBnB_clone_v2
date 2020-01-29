#!/usr/bin/python3
"""
starts a Flask web application
"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
import sys

# host = sys.getenv("HBNB_API_HOST")
# port = sys.getenv("HBNB_API_PORT")

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 handler """
    return {"error": "Not found"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
