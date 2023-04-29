#!/usr/bin/python3
"""creates the app routes"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv('HBNB_API_HOST', default='0.0.0.0')
port = getenv('HBNB_API_PORT', default='5000')


@app.teardown_appcontext
def remove_session(exception):
    """method that closes the database connection"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handler that returns json-formatted 404 code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True, threaded=True)
