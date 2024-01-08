#!/usr/bin/python3
"""
this module is to use CORs for api testing
"""
from api.v1.views import app_views
import sys
from flask import Flask
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Calls storage.close() upon teardown."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
