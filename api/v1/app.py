#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown():
    """
    calls the storage.close() insatnce
    """
    storage.close()
    
if __name__ == "__main__":
    """
    run flask server
    """
    host = '0.0.0.0' or 'HBNB_API_HOST'
    port = '5000' or 'HBNB_API_PORT'
    
    app.run(host, port, threaded=True)