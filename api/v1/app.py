from flask import Flask, make_response, jsonify
from models import storage
from os import environ
from api.v1.views import app_views
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "http://0.0.0.0"}})

@app.errorhandler(404)
def nop(e):
    return make_response(jsonify({"error":"Not Found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB Clone Restful API',
    'uiversion': 3
}

Swagger(app)

@app.teardown_appcontext
def close(self):
    """close storage"""
    storage.close()

if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
