#!/usr/bin/python3
"""app module"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)

API_HOST = os.getenv("HBNB_API_HOST", default='0.0.0.0')
API_PORT = os.getenv("HBNB_API_PORT", default=5000)


@app.teardown_appcontext
def teardown_appcontext(exception):
	"""close storage"""
	storage.close()


if __name__ == "__main__":
	app.run(host=API_HOST, port=API_PORT, threaded=True)
