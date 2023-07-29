#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views

# Create a Flask instance
app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# Declare a method to handle @teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def close_storage(exception):
    storage.close()


if __name__ == "__main__":

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
