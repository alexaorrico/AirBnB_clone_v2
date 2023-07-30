from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)

# Register the Blueprint for v1 views
app.register_blueprint(app_views)

if __name__ == "__main__":
    app.run(debug=True)
