#!/user/bin/python3
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def Teardown(self):
    """ calls storage close method """
    storage.close()

@app.errorhandler(404)
def error_handler(error):
    """mondá """
    error_dict = {"error": "Not found"}
    return jsonify(error_dict)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
