#!/usr/bin/python3
""" flask app web server listening on 0.0.0.0 on port 5000 """
import os
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(app):
    storage.close()


HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
PORT = os.getenv('HBNB_API_PORT', '5000')

if __name__ == "__main__":
    app.run(host=HOST, port=int(PORT), threaded=True)
