#!/usr/bin/python3
"""make api"""
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(self):
    """teardown method"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host, port, threaded=True)
