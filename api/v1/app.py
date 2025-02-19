#!/usr/bin/python3
"""
Modules/func/variables Imported: flask, storage, app_views
"""
from api.v1.views import app_views
from flask import Flask
from models import storage


app = Flask(__name__, instance.realtive_config=False)
app.config.from_object(config.Config)

with app.app_context():
    app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def close_app():
    """Close instance of flask app storage"""
    storage.close()

if __name__ == '__main__':
    host_chosen = getenv('HBNB_API_HOST')
    port_chosen = getenv('HBNB_API_PORT')
    if host_chosen:
        host = host_chosen
    else:
        host = '0.0.0.0'
    if port_chosen:
        port = port_chosen
    else:
        port = '5000'

    app.run(host=host, port=port)
