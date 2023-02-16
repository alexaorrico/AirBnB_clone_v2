#!/usr/bin/python3


from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

HBNB_API_HOST = "0.0.0.0"
HBNB_API_PORT = 5000

def close_storage(exception=None):
    """"performs clea up tasks"""
    storage.close()

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    close_storage(exception)

if __name__ = "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
