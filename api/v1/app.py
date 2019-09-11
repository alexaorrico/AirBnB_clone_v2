#!/usr/bin/python3
"""
starts a Flask web application
"""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_404(err):
    """status render template for json"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    """init of the flask app"""

    app.run(host='0.0.0.0', port='5000', threaded=True)
