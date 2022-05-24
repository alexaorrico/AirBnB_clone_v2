#!/usr/bin/python3
"""status of an api"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(exception):
	"""manages storafe"""
	storage.close()


@app.errorhandler(404)
def not_found(error):
	"""handles error 404"""
	return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
	host = getenv("HBNB_API_HOST", "0.0.0.0")
	port = getenv("HBNB_API_PORT", "5000")
	app.run(host=host, port=port, threaded=True, debug=True)
