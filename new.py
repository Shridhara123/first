from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "nale office barthira hello"
    })

# NEW FEATURE
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "version": "2.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)