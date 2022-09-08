#!/usr/bin/python3
"""
"""
from models import storage
from flask import Flask
from api.v1.views import app_views

app.register_blueprint(app_views)

app = Flask(__name__)

@app.teardown_appcontext
def s_close():
    """
    """
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv(HBNB_API_HOST, 0.0.0.0),
	    port=getenv(HBNB_API_HOST, 5000), threaded=True)
