#!/usr/bin/python3
"""
file app for starting FLask
registering blueprint 
"""
from os import getenv

from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """
    to close query zfter each session
    """
    storage.close()


@app.errorhandler
def error_handler(self):
    """
    return 404 status code response when error
    """


if __name__ == "__main__":
    """ app listening on host 0.0.0.0 and port 5000 """
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
