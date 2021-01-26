#!/usr/bin/python3
"""Status of your API"""
from flask import Flask
from api.v1.views import app_views
from models import storage 
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_app(self):
    """" method that calls storage.close()"""
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=getenv("BNB_API_PORT",default="5000"), 
            threaded=True)
