from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
# Cross-Origin Resource Sharing
host = '0.0.0.0'
cors = CORS(app, resources={r'/*': {'origins': host}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    this method calls storage.close() function
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
