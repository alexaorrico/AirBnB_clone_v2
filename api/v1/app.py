"""
    register app in blueprint
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == "__main__":
    #Get host and port from environment variables or use default values
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    #Run the Flask app with the specified options
    app.run(host=host, port=port, threaded=True)
