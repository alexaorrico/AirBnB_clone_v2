#!/usr/bin/python3
"""
Starts up a copy of a flask-app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(self):
    """Closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return {"error": "Not found"}, 404

if __name__ =="__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_HOST", 5000))
    app.run(host=host, port=port, threaded=True)
