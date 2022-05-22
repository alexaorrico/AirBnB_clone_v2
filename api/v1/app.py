#!/usr/bin/python3
"""Module for task 4"""


from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask()
app.register_blueprint(app_views)

@app.teardown_appcontext
storage.close()

if __name__ == "__main__":
    if $HBNB_API_HOST is None:
        host = 0.0.0.0
    else:
        host = $HBNB_API_HOST
    if $HBNB_API_PORT is None:
        port = 5000
    else:
        port = $HBNB_API_PORT
    threaded = True
    app.run(host, port)
