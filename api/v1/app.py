#!/usr/bin/python3
"""
Status of your API
"""

from os import getenv
from models import storage
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
HBNB_API_PORT = getenv('HBNB_API_PORT' , '5000')

@app.teardown_appcontext
def storage_close():
    """
    Calls storage.close()
    """
    
    storage.close()


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=
            HBNB_API_PORT, threaded=True)
