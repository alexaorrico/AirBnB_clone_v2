#!/usr/bin/python3
from flask.app import Flask
app = Flask(__name__)
print(dir(app))
@app.post('/404')
def error():
    print(app.route)
    return "exception"
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", threaded=True)
