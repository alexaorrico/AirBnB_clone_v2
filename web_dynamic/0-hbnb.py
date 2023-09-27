#!/usr/bin/python3
""" Starts a Flask Web Application """

from flask import Flask, render_template
import uuid


app = Flask(__name__)


@app.route('/0-hbnb', strict_slashes=False)
def hbnb():
  """ Render Template """

  return render_template('0-hbnb.html', cache_id=str(uuid.uuid4()))


if __name__ == "__main__":
    """ Run port """
    app.run(host='0.0.0.0', port=5001)