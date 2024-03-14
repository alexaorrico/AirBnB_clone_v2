from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger

# Create Flask app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Teardown app context
@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

# 404 Error handler
@app.errorhandler(404)
def not_found(error):
    """ 404 Error """
    return make_response(jsonify({'error': "Not found"}), 404)

# Configure Swagger
app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}
Swagger(app)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST') or '0.0.0.0'
    port = int(environ.get('HBNB_API_PORT') or 5000)
    app.run(host=host, port=port, threaded=True)
