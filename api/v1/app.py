from flask import Flask
import os
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
