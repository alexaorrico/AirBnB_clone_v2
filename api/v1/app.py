#!/usr/bin/python3
"""Creating Flask app"""


from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
if __name__ == "__main__":
    HOST = getenv()
    PORT = int(getenv())
    app.run(host=HOST, prot=PORT, threaded=True)
