
import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

# Create the Flask app instance
app = Flask(__name__)

app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
# Register the blueprint for the views
app.register_blueprint(app_views)
# Enable CORS for all routes under origin
CORS(app, resources={'/*': {'origins': app_host}})


# Close the storage session after each request
@app.teardown_appcontext
def close_storage(error):
    """Close the storage session"""
    storage.close()


# Handle 404 errors with a custom JSON response
@app.errorhandler(404)
def not_found(error):
    """Return a JSON error message for 404"""
    return jsonify({'error': 'Not found'}), 404


# Handle 400 errors with a custom JSON response
@app.errorhandler(400)
def bad_request(error):
    """Return a JSON error message for 400"""
    message = 'Bad request'
    if isinstance(error, Exception) and error.description:
        message = error.description
    return jsonify({'error': message}), 400


# Run the app if executed as the main script
if __name__ == '__main__':
    app.run(
        host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(os.getenv('HBNB_API_PORT', '5000')),
        threaded=True
    )
