 #!/usr/bin/python3
 
"""Contains the API and flask instance"""
from models import Storage
from flask import Flask

app = Flask(__name__)

from api.v1.views import app_views
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(exc):
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
