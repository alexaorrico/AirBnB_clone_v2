#!/usr/bin/python3
from flask import Flask
import os
from models import storage
from api.v1.views import app_views

# We create an instance of the Flask application.
app = Flask(__name__)

# We register the routes defined in 'app_views' in our application.
app.register_blueprint(app_views)

# This function will be executed when the application context is closed.
@app.teardown_appcontext
def teardown_appcontext(exception):
    # We close the connection with the database.
    storage.close()

# We check if we are running this script directly.
if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
