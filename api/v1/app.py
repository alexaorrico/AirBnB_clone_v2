#!/usr/bin/python3
"""
text
"""
from flask import Flask
import models
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = 5000


@app.teardown_appcontext
def close_db(self):
    """text"""
    storage.close()


if __name__ == "__main__":
    app.run(HBNB_API_HOST, HBNB_API_PORT,
            debug=True, threaded=True)
