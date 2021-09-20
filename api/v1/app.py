#!/usr/bin/python3
""" flask API app """
from models import storage
from flask import Flask, json
from flask_cors import CORS, cross_origin
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(HTTPException)
def handle_404(e):
    """ return 404 NOT found as JSON """
    response = e.get_response()
    response.data = json.dumps({"error": "Not found"})
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    """ run the flask server """
    app.run(host='0.0.0.0', port=5000, threaded=True)
