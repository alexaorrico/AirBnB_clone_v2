#!/usr/bin/python3
"""Flask app to generate html list of all states from storage"""
from flask import Flask, render_template
from models import storage
app = Flask('web_flask')
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def list_of_states():
    """Render as html alphabetical list of states and cities in each state
    from `storage`"""
    states = storage.all('State')
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(*args, **kwargs):
    """Close database or file storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
