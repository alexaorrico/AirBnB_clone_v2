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

@app.teardown_appcontext
def storage_close(self):
    """
    Calls storage.close()
    """
    
    storage.close()


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT' , '5000')
    app.run(host=HOST, port=PORT, threaded=True)
