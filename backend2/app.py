# https://flask.palletsprojects.com/en/stable/quickstart/ (supports:    @app.route(...), request.get_json(), jsonify(...)
# https://flask-cors.readthedocs.io/en/latest/   (supports: from flask_cors import CORS, CORS(app))
# https://www.psycopg.org/docs/usage.html     (supports: psycopg2.connect(...), SQL execution, cursor usage)
# https://supabase.com/docs/guides/database/connecting-to-postgres   (supports: DATABSE_URL, aka connection string)

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")


@app.route("/")
def home():
    return "Backend running"

# run to see if connected
@app.route("/test-db")
def test_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"success": True, "result": result[0]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/roster")
def get_roster():
    try:
# python chit chat with database
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
#SELECT.... FROM table;  (SQL select queries
        cur.execute("SELECT id, student_name, bus_id, grade FROM roster ORDER BY id;")
        rows = cur.fetchall()
#loop through database section and conver to JSON   (JSON format using Flask’s jsonify)
        roster_list = []
        for row in rows:
            roster_list.append({
                "id": row[0],
                "student_name": row[1],
                "bus_id": row[2],
                "grade": row[3]
            })

        cur.close()
        conn.close()

        return jsonify(roster_list)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })






@app.route("/check-in", methods=["POST"])
def check_in():
    try:
        data = request.get_json()

        student_name = data.get("student_name", "").strip()
        bus_id = data.get("bus_id", "").strip()

        if student_name == "" or bus_id == "":
            return jsonify({
                "success": False,
                "error": "student_name and bus_id are required"
            }), 400

        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        cur.execute(
            """
            insert into student_checkins (student_name, bus_id)
            values (%s, %s)
            returning id, student_name, bus_id, created_at;
            """,
            (student_name, bus_id)
        )

        new_row = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Check-in saved",
            "checkin": {
                "id": new_row[0],
                "student_name": new_row[1],
                "bus_id": new_row[2],
                "created_at": str(new_row[3])
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
