#!/usr/bin/python3
"""
create a variable app, instance of Flask
import storage from models
import app_views from api.v1.views
register the blueprint app_views to your Flask instance app
declare a method to handle @app.teardown_appcontext
that calls storage.close()
inside if __name__ == "__main__":, run your
Flask server (variable app) with:
    host = environment variable HBNB_API_HOST
    or 0.0.0.0 if not defined
    port = environment variable HBNB_API_PORT or
    5000 if not defined
    threaded=True
"""

from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
