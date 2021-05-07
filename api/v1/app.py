#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """ a method that calls storage.close """
    storage.close()

if __name__ == '__main__':
    if not HBNB_API_HOST:
        HBNB_API_HOST = "0.0.0.0"
    if not HBNB_API_PORT:
        HBNB_API_PORT = "5000"
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
