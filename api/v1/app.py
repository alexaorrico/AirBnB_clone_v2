#!/usr/bin/python3
"""
Flask App for the HBNB API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == "__main":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
