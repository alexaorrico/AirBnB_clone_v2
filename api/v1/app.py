#!/usr/bin/python3
#Michael edited 11/19 8:21 PM
"""API"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app_views = Blueprint("app_views", __name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown():
    """closes application"""
    storage.close()

if __name__ == "__main__":
    host = os.environ.et("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
