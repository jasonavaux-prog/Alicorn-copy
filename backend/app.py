from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
#is an HTTP-header based mechanism that allows a server to indicate any origins 
#https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
#simple version: CORS allows use of fetch(), it gives permission for the browser to accept the data from another origin
CORS(app)

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
