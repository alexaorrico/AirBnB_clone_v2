#!/usr/bin/python3
"""Create method closed and the server"""


from flask import Flask
from models import storage
from api.v1.views import app_views
import os
HOST = os.getenv('HBNB_API_HOST')
PORT = os.getenv('HBNB_API_PORT')


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def closed(exit):
    """close storage"""
    storage.close()

@app.errorhandler(404)
def error_404(error):
    return {"error": "Not found"}


if __name__ == "__main__":
    app.run(host='HBNB_API_HOST' or '0.0.0.0', port='HBNB_API_PORT' or '5000',
            threaded=True, debug=True)
            port=int(os.getenv('HBNB_API_PORT', '5000')))