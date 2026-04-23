# https://flask.palletsprojects.com/en/stable/quickstart/
# https://flask-cors.readthedocs.io/en/latest/
# https://www.psycopg.org/docs/usage.html
# https://supabase.com/docs/guides/database/connecting-to-postgres

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")


@app.route("/")
def home():
    return "ALICORN backend running"


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
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/roster")
def get_roster():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        cur.execute("SELECT id, student_name, bus_id, grade FROM roster ORDER BY id;")
        rows = cur.fetchall()

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
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/attendance")
def get_attendance():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        cur.execute("""
            SELECT id, student_name, bus_id, created_at, date, status
            FROM attendance
            ORDER BY id DESC;
        """)
        rows = cur.fetchall()

        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "student_name": row[1],
                "bus_id": row[2],
                "created_at": str(row[3]),
                "date": str(row[4]) if row[4] is not None else None,
                "status": row[5]
            })

        cur.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/attendance", methods=["POST"])
def add_attendance():
    try:
        data = request.get_json()

        student_name = data.get("student_name")
        bus_id = data.get("bus_id")
        date = data.get("date")
        status = data.get("status")

        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO attendance (student_name, bus_id, date, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id, student_name, bus_id, created_at, date, status;
            """,
            (student_name, bus_id, date, status)
        )

        new_row = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "row": {
                "id": new_row[0],
                "student_name": new_row[1],
                "bus_id": new_row[2],
                "created_at": str(new_row[3]),
                "date": str(new_row[4]) if new_row[4] is not None else None,
                "status": new_row[5]
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
