"""
CREATED 4/18/2026
Update 4/22/2026
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
#psy for database or db for short
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = "postgresql://postgres.phpgxdpdsujisdnbtmcm:0mLKcJUphyg85yKx@aws-1-us-east-1.pooler.supabase.com:5432/postgres"

print("👉 Using DB:", DATABASE_URL)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT 1;")
    print("✅ Connected:", cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ ERROR:", e)
    
    
    

# app.jsx will "fetch" request the URL in app.py  
# EXAMPLE: fetch("http://localhost:5000/bus-location")      

# that fetch hits backend, /bus-location as shown below

# App.jsx sends a fetch request to the Flask backend URL (/bus-location).
# This request is handled by app.py using a route.
# The route returns JSON data back to the frontend.

@app.route("/bus-location", methods=["GET"])
def bus_location():
    # sends JSON back to front end
    return jsonify(current_bus_location)



# ----------------------------------
# ATTENDANCE DATA
# ----------------------------------
@app.route("/attendance", methods=["GET"])
def attendance():
    return jsonify([
        {"studentId": "1001", "name": "Jordan Lee", "status": "On Bus"},
        {"studentId": "1002", "name": "Taylor Smith", "status": "Absent"}
    ])



# ----------------------------------
# STUDENT LIST
# ----------------------------------
@app.route("/students", methods=["GET"])
def students():
    return jsonify([
        {"studentId": "1001", "name": "Jordan Lee", "route": "Route A"},
        {"studentId": "1002", "name": "Taylor Smith", "route": "Route B"}
    ])



# ----------------------------------
# RECEIVE GPS DATA FROM FRONTEND
# ----------------------------------
#this will write the data
@app.route("/gps", methods=["POST"])
def gps():
    data = request.get_json()

    # check if data was sent
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # update stored bus location
    current_bus_location["busId"] = data.get("busId", current_bus_location["busId"])
    current_bus_location["latitude"] = data.get("latitude", current_bus_location["latitude"])
    current_bus_location["longitude"] = data.get("longitude", current_bus_location["longitude"])
    current_bus_location["status"] = data.get("status", current_bus_location["status"])

    print("GPS DATA:", data)

    return jsonify({
        "status": "received",
        "busLocation": current_bus_location
    })

# ----------------------------------
# STORE CURRENT BUS LOCATION
# ----------------------------------
#this will read data
current_bus_location = {
    "busId": "12",
    "latitude": 38.8816,
    "longitude": -77.0910,
    "status": "On Route"
}


# ----------------------------------
# RUN SERVER (local + Render)
# ----------------------------------

if __name__ == "__main__":
    app.run(debug=True)

#if __name__ == "__main__":
#    PORT = int(os.environ.get("PORT", 5000))
#    app.run(host="0.0.0.0", port=PORT)
