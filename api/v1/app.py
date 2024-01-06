#!/usr/bin/python3
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext()
def teardown_appcontext(exception):
    storage.close()
    
if __name__ == '__main__':
    HOST = '0.0.0.0' if getenv('HBNB_API_HOST') is None else getenv('HBNB_API_HOST')
    PORT = '5000' if getenv('HBNB_API_PORT') is None else getenv('HBNB_API_PORT')
    app.run(host=HOST, port=PORT, threaded=True)