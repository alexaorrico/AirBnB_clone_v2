#!/usr/bin/python3
"""
Module app
"""
from flask import Flask
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
        from models import storage
        storage.close()


if __name__ == '__main__':
        app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
                port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
