from flask import Flask, request, jsonify, make_response
import sqlite3
import os
from io import StringIO

app = Flask(__name__)
DATABASE = 'sensor_data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript('''
        -- Table for sensor details (ID and location)
        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id INTEGER PRIMARY KEY,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        );
        
        -- Table for sensor types and their units
        CREATE TABLE IF NOT EXISTS sensor_types (
            type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_type TEXT NOT NULL UNIQUE,
            unit TEXT NOT NULL
        );
        
        -- Table for measurement data, linked to sensors and sensor types
        CREATE TABLE IF NOT EXISTS measurements (
            measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            value REAL NOT NULL,
            FOREIGN KEY(sensor_id) REFERENCES sensors(sensor_id),
            FOREIGN KEY(type_id) REFERENCES sensor_types(type_id)
        );
        ''')

@app.route('/submit', methods=['POST'])
def submit_sensor_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Expected JSON payload:
    # {
    #   "sensor_id": 1,
    #   "sensor_location": {"latitude": 12.34, "longitude": 56.78},
    #   "sensor_type": "Temperature",
    #   "unit": "°C",
    #   "timestamp": "2025-02-24 12:34",
    #   "value": 13.9
    # }
    sensor_id = data.get("sensor_id")
    location = data.get("sensor_location", {})
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    sensor_type = data.get("sensor_type")
    unit = data.get("unit")
    timestamp = data.get("timestamp")
    value = data.get("value")

    if None in [sensor_id, latitude, longitude, sensor_type, unit, timestamp, value]:
        return jsonify({"error": "Missing fields"}), 400

    with get_db() as conn:
        # Insert the sensor if it doesn't exist already.
        conn.execute('''
            INSERT OR IGNORE INTO sensors (sensor_id, latitude, longitude)
            VALUES (?, ?, ?)
        ''', (sensor_id, latitude, longitude))

        # Insert the sensor type if it's new.
        conn.execute('''
            INSERT OR IGNORE INTO sensor_types (sensor_type, unit)
            VALUES (?, ?)
        ''', (sensor_type, unit))
        
        # Retrieve the type_id from sensor_types.
        cur = conn.execute('SELECT type_id FROM sensor_types WHERE sensor_type = ?', (sensor_type,))
        type_row = cur.fetchone()
        type_id = type_row['type_id']

        # Insert the measurement data.
        conn.execute('''
            INSERT INTO measurements (sensor_id, type_id, timestamp, value)
            VALUES (?, ?, ?, ?)
        ''', (sensor_id, type_id, timestamp, value))
        conn.commit()
    return jsonify({"status": "success"}), 201

@app.route('/retrieve', methods=['GET'])
def retrieve_sensor_data():
    sensor_id = request.args.get("sensor_id")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    if not sensor_id or not start_time or not end_time:
        return jsonify({"error": "Missing query parameters"}), 400

    with get_db() as conn:
        # Join measurements with sensor_types to include type and unit info.
        cursor = conn.execute('''
            SELECT st.sensor_type, st.unit, m.timestamp, m.value
            FROM measurements m
            JOIN sensor_types st ON m.type_id = st.type_id
            WHERE m.sensor_id = ? AND m.timestamp BETWEEN ? AND ?
            ORDER BY m.timestamp ASC
        ''', (sensor_id, start_time, end_time))
        rows = cursor.fetchall()

    # Group the data by sensor type.
    grouped = {}
    for row in rows:
        stype = row["sensor_type"]
        if stype not in grouped:
            grouped[stype] = {"unit": row["unit"], "data": []}
        grouped[stype]["data"].append({
            "timestamp": row["timestamp"],
            "value": row["value"]
        })
    return jsonify(grouped)

@app.route('/fetch', methods=['GET'])
def fetch_sensor_type_data():
    sensor_type = request.args.get("type")
    if not sensor_type:
        return jsonify({"error": "Missing sensor type parameter"}), 400

    with get_db() as conn:
        # Retrieve all measurements for the given sensor type.
        cursor = conn.execute('''
            SELECT s.sensor_id, s.latitude, s.longitude, st.sensor_type, st.unit, m.timestamp, m.value
            FROM measurements m
            JOIN sensor_types st ON m.type_id = st.type_id
            JOIN sensors s ON m.sensor_id = s.sensor_id
            WHERE st.sensor_type = ?
            ORDER BY m.timestamp ASC
        ''', (sensor_type,))
        rows = cursor.fetchall()

    output = StringIO()
    for row in rows:
        output.write(f"{row['sensor_id']}, {row['latitude']}, {row['longitude']}, "
                     f"{row['sensor_type']}, {row['unit']}, {row['timestamp']}, {row['value']}\n")
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=data.txt"
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

