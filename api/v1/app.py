#!/usr/bin/python3
"""
Creates an instances of Flask,
creates Blueprint instance,
and handles teardown
"""

from api.v1.views import app_views
from models import storage
from flask import Flask

host = 'HBNB_API_HOST' or 0.0.0.0 if not in defined
port = 'HBNB_API_PORT' or 5000 if not in defined

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    return storage.close()

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host=host, port=port)
