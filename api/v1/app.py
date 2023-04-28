from models import storage
from flask import Flask
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
