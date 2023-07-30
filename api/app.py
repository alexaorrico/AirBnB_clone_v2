# Create a folder api at the root of the project with an empty file __init__.py

# Create a folder v1 inside api:
# create an empty file __init__.py

# Create a file app.py:
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage():
    storage.close()

if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)

# Create a folder views inside v1:

# create a file __init__.py:
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# wildcard import of everything in the package api.v1.views.index => PEP8 will complain about it, don’t worry, it’s normal and this file (v1/views/__init__.py) won’t be check.

from .index import *

# Create a file index.py:
from flask import jsonify

@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
