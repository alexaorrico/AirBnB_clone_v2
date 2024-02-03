#!/usr/bin/python3
"""
controller web flask app
"""
from flask import jsonify
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """close the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """return 404 json for uknown ressources"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
