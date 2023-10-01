from flask import Flask
from models import storage
from api.v1.views import app_views
import os

#flask app instance
app = Flask(__name__)

#blueprint registration
app.register_blueprint(app_views)

#teardown method
@app.teardown_appcontext
def teardown_appcontext(exception):
    """close running SQLAlchemy session"""
    storage.close()

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
