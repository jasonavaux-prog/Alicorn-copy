from flask import Flask, request, jsonify
from flask_cors import CORS
#added socket + os for live demo
from flask_socketio import SocketIO, emit
import os



app = Flask(__name__)
#https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
#CORS for normal Flask routes like /bus-location, /attendance, /students, /gps
CORS(app)

# Socket.IO setup for live events
socketio = SocketIO(app, cors_allowed_origins="*")

#route() decorator to tell Flask what URL should trigger our function. (source flask quickstart)
@app.route("/")
def home():
    return "ALICORN backend is running"



"""\
CREATED 4/18/2026
@app.route("/bus-location", methods=["GET"])
@app.route("/attendance", methods=["GET"])
@app.route("/students", methods=["GET"])
@app.route("/gps", methods=["POST"])

added socket.io (this for GPS) - 4/21/2026


Update 4/20/2026
"""


# app.jsx will "fetch" request the URL in app.py  (current just use your comp as localhost in example)  EXAMPLE: fetch("http://localhost:5000/bus-location")      
# that fetch hits backend, /bus-location as shown below

#App.jsx sends a fetch request to the Flask backend URL (/bus-location).
#This request is handled by app.py using a route.
#The route returns JSON data back to the frontend.

@app.route("/bus-location", methods=["GET"])
def bus_location():
# sends JSON back to front end
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

''' OLD STATIC
@app.route("/gps", methods=["POST"])
def gps():
    data = request.get_json()
    print("GPS DATA:", data)
    return jsonify({
        "status": "received",
        "data": data
    })
'''


@app.route("/gps", methods=["POST"])
def gps():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update stored demo location
    current_bus_location["busId"] = data.get("busId", current_bus_location["busId"])
    current_bus_location["latitude"] = data.get("latitude", current_bus_location["latitude"])
    current_bus_location["longitude"] = data.get("longitude", current_bus_location["longitude"])
    current_bus_location["status"] = data.get("status", current_bus_location["status"])

    print("GPS DATA:", data)

    # Also push update live to all connected socket clients
    socketio.emit("location_update", current_bus_location)

    return jsonify({
        "status": "received",
        "data": current_bus_location
    })

# Live Socket.IO version
@socketio.on("send_location")
def handle_send_location(data):
    if not data:
        return

    current_bus_location["busId"] = data.get("busId", current_bus_location["busId"])
    current_bus_location["latitude"] = data.get("latitude", current_bus_location["latitude"])
    current_bus_location["longitude"] = data.get("longitude", current_bus_location["longitude"])
    current_bus_location["status"] = data.get("status", current_bus_location["status"])

    print("LIVE SOCKET GPS DATA:", data)

    emit("location_update", current_bus_location, broadcast=True)
#live run
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=PORT, debug=True)

''' OLD STATIC
if __name__ == "__main__":
    app.run(debug=True)
'''
