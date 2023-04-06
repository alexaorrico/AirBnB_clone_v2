#!/usr/bin/python3
"""Module"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.book import Book
from models.author import Author
from models.publisher import Publisher


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exc):
    """Close the current SQLAlchemy session"""
    storage.close()


@app.route('/status')
def status():
    """
    returns a JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})


@app.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    return jsonify({
        "books": storage.count(Book),
        "authors": storage.count(Author),
        "publishers": storage.count(Publisher)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
