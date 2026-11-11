from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    app.logger.info("SERVICERUNNING")
    return jsonify({"message": "OpenShift CI/CD sample application"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
