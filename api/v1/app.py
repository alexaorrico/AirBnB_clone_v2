from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from api.v1.views import app_views

app = Flask(__name)
app.url_map.strict_slashes = False

# Register your blueprint (app_views) here

# Define a handler for 404 errors
@app.errorhandler(HTTPException)
def handle_404_error(e):
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
