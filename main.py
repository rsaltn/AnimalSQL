
from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    image = data.get('image')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO environment_data (temperature, humidity, image, timestamp) VALUES (%s, %s, %s, %s)",
        (temperature, humidity, image, datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/latest_data', methods=['GET'])
def latest_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT temperature, humidity, image, timestamp FROM environment_data ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return jsonify({
            "temperature": row[0],
            "humidity": row[1],
            "image": row[2],
            "timestamp": row[3].isoformat()
        })
    else:
        return jsonify({"error": "no data"}), 404

if __name__ == '__main__':
    app.run(debug=True)
