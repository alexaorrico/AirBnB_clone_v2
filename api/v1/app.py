#!/usr/bin/python3

"""
Module Aplication
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

app.strict_slashes = False


@app.teardown_appcontext
def closeMethod(exception=None):
    """Method for close session"""
    storage.close()

if __name__ == '__main__':
    app.run(host=os.eviron['0.0.0.0'],
            port=os.eviron['5000'],
            threaded=True)
