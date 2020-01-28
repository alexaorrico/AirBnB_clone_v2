from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask()


@app.teardown_appcontext
def teardown():
    storage.close()


if __name__ == "__main__":
    app.run(
        debug=True,
        host=os.getenv("HBNB_API_HOST") or "0.0.0.0",
        port=int(os.getenv("HBNB_API_PORT")) or 5000,
        threaded=True
    )
