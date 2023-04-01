from flask import Flask
from api.v1.views import app_views
from models import storage

# create Flask instance
app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)

# define teardown method
@app.teardown_appcontext
def teardown_storage(exception):
    storage.close()

# start Flask server
if __name__ == "__main__":
    import os
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
