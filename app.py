from flask import Flask, request, render_template, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="manager",  # Set your MySQL password
        database="gift_registry"
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_registry():
    name = request.form['name']
    date = request.form['date']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registries (name, event_date) VALUES (%s, %s)", (name, date))
    conn.commit()
    registry_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return redirect(url_for('add_gift', registry_id=registry_id))

@app.route('/add-gift')
def add_gift():
    registry_id = request.args.get('registry_id')
    return render_template('add_gift.html', registry_id=registry_id)

@app.route('/add-gift', methods=['POST'])
def submit_gift():
    registry_id = request.form['registry_id']
    gift_name = request.form['gift_name']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gifts (registry_id, name) VALUES (%s, %s)", (registry_id, gift_name))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view_registry', registry_id=registry_id))

@app.route('/view')
def view_registry():
    registry_id = request.args.get('registry_id')
    return render_template('view_registry.html', registry_id=registry_id)

@app.route('/api/gifts')
def api_gifts():
    registry_id = request.args.get('registry_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, purchased FROM gifts WHERE registry_id = %s", (registry_id,))
    gifts = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(gifts)

if __name__ == '__main__':
    app.run(debug=True)
