#!/usr/bin/python3
"""
A script that starts a flask app and / returns “Hello HBNB!”
"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
# register blueprint app_views
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_storage(exception):
    """
    This method closes storage instance
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    Return "error": "Not found"
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
