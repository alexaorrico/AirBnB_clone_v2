from flask import Flask

app = Flask(__name__)

@app.route("/states", methods=["GET"])
def get_states():
    return jsonify({"states": states})

if __name__ == "__main__":
    app.run()
