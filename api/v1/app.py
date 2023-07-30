#!/usr/bin/python3
"""Flask web service API"""

from flask import Flask

import os
from models import storage
from api.v1.views import app_views  # Blueprint

app = Flask(__name__)

# Register app_views as blueprint to app
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error=None):
    """ Called when application context is torn down"""
    storage.close()


if __name__ == "__main__":
    app.run(host=(os.getenv('HBNB_API_HOST', '0.0.0.0')),
            port=(int(os.getenv('HBNB_API_PORT', '5000'))),
            threaded=True)
