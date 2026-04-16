from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "ALICORN backend is running"

@app.route("/gps", methods=["POST"])
def gps():
    data = request.get_json()
    print("GPS DATA:", data)
    return jsonify({"status": "received", "data": data})

if __name__ == "__main__":
    app.run(debug=True)
