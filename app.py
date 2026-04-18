from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "ALICORN backend is running"

@app.route("/bus-location", methods=["GET"])
def bus_location():
    return jsonify({
        "busId": "12",
        "latitude": 38.8816,
        "longitude": -77.0910,
        "status": "On Route"
    })

@app.route("/attendance", methods=["GET"])
def attendance():
    return jsonify([
        {"studentId": "1001", "name": "Jordan Lee", "status": "On Bus"},
        {"studentId": "1002", "name": "Taylor Smith", "status": "Absent"}
    ])

@app.route("/students", methods=["GET"])
def students():
    return jsonify([
        {"studentId": "1001", "name": "Jordan Lee", "route": "Route A"},
        {"studentId": "1002", "name": "Taylor Smith", "route": "Route B"}
    ])

@app.route("/gps", methods=["POST"])
def gps():
    data = request.get_json()
    print("GPS DATA:", data)
    return jsonify({
        "status": "received",
        "data": data
    })

if __name__ == "__main__":
    app.run(debug=True)
