#!/usr/bin/python3
"""
    Main file of API,
    he store the Flask app and run the api
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources=r'/*', origins="0.0.0.0")


@app.teardown_appcontext
def teardown(self):
    ''' Remove the current SQLAlchemy Session '''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Use errorhandler to display 404 error page"""
    return jsonify({"error": "Not found"}), 404


# Run the app with the default port 5000 threaded true
if __name__ == '__main__':
    host = getenv(
        "HBNB_API_HOST", "0.0.0.0"
    )
    port = getenv(
        "HBNB_API_PORT", 5000
    )
    app.run(host=host, port=port, threaded=True)
