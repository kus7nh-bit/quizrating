from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "ratings.db"


# ========================================
# DATABASE CONNECTION
# ========================================

def get_db():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


# ========================================
# CREATE DATABASE
# ========================================

def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_name TEXT NOT NULL,
            question TEXT NOT NULL,
            rating INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ========================================
# HOME PAGE
# ========================================

@app.route("/")
def index():

    return render_template("index.html")


# ========================================
# SUBMIT SURVEY
# ========================================

@app.route("/submit", methods=["POST"])
def submit():

    try:

        data = request.get_json()

        person_name = data.get("personName")
        answers = data.get("answers", [])


        if not person_name:

            return jsonify({
                "success": False,
                "message": "Please enter your name."
            }), 400


        if not answers:

            return jsonify({
                "success": False,
                "message": "Please answer all questions."
            }), 400


        conn = get_db()


        for answer in answers:

            conn.execute("""
                INSERT INTO responses
                (
                    person_name,
                    question,
                    rating,
                    created_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                person_name,
                answer["question"],
                answer["rating"],
                datetime.now().isoformat()
            ))


        conn.commit()
        conn.close()


        return jsonify({
            "success": True,
            "message": "Submitted successfully!"
        })


    except Exception as e:

        print("SUBMIT ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ========================================
# RESPONSES PAGE
# ========================================

@app.route("/responses")
def responses():

    return render_template("responses.html")


# ========================================
# GET ALL PEOPLE
# ========================================

@app.route("/people")
def people():

    conn = get_db()

    rows = conn.execute("""
        SELECT DISTINCT person_name
        FROM responses
        ORDER BY person_name
    """).fetchall()

    conn.close()


    people = [
        row["person_name"]
        for row in rows
    ]


    return jsonify(people)


# ========================================
# GET PERSON'S RESPONSES
# ========================================

@app.route("/responses/<person_name>")
def person_responses(person_name):

    conn = get_db()

    rows = conn.execute("""
        SELECT question, rating
        FROM responses
        WHERE person_name = ?
        ORDER BY id
    """, (person_name,)).fetchall()

    conn.close()


    responses = []

    for row in rows:

        responses.append({
            "question": row["question"],
            "rating": row["rating"]
        })


    return jsonify(responses)


# ========================================
# START APPLICATION
# ========================================

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )