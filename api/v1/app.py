#!/usr/bin/python3


from models import storage
from api.v1.views import app_views
from flask import Flask
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def call_close():
    return storage.close()

if __name__ == "__main__":
    app.run(os.environ.get('HBNB_API_HOST'), os.environ.get('HBNB_API_PORT'), threaded=True)