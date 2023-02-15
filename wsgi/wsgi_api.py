#!/usr/bin/python3
"""
imports API App for gunicorn configurations
gunicorn --bind 127.0.0.1:8004 wsgi.wsgi_api:app
"""
app = __import__('api.v1.app', globals(), locals(), ['*'])

if __name__ == "__main__":
    """runs the main flask app"""
    app.app.run()
