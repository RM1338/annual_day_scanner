from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-to-something-random-123456'

# Dashboard password
DASHBOARD_PASSWORD = "admin2025"


def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS families
                 (family_id TEXT PRIMARY KEY, 
                  student1_name TEXT,
                  student1_admno TEXT,
                  class TEXT,
                  section TEXT,
                  student2_name TEXT,
                  student2_admno TEXT,
                  parents TEXT,
                  phone TEXT,
                  data_json TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS scans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  family_id TEXT,
                  scan_type TEXT,
                  timestamp TEXT,
                  gate_number TEXT,
                  person_count INTEGER DEFAULT 1)''')

    conn.commit()
    conn.close()
    print("✅ Database initialized!")


def load_sample_data():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM families")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    families = [
        ("FAM-2025-0001", "Rahul Kumar", "A12345", "10", "A", "", "",
         "Mr. Suresh Kumar, Mrs. Anita Kumar", "9876543210", "{}"),
        ("FAM-2025-0002", "Priya Sharma", "A12346", "9", "B", "Rohan Sharma", "A12399",
         "Mr. Amit Sharma, Mrs. Neha Sharma", "9876543211", "{}"),
        ("FAM-2025-0003", "Anjali Patel", "A12347", "11", "C", "", "",
         "Mr. Rajesh Patel, Mrs. Meera Patel", "9876543212", "{}"),
    ]

    c.executemany('''INSERT INTO families VALUES (?,?,?,?,?,?,?,?,?,?)''', families)
    conn.commit()
    conn.close()
    print("✅ Sample data loaded!")


# Scanner page
@app.route('/')
def index():
    return render_template('scanner.html')


# Dashboard login
@app.route('/dashboard-login')
def dashboard_login():
    return render_template('dashboard_login.html')


# Dashboard auth
@app.route('/dashboard-auth', methods=['POST'])
def dashboard_auth():
    try:
        password = request.json.get('password')
        if password == DASHBOARD_PASSWORD:
            session['dashboard_access'] = True
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid password'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('dashboard_access'):
        return redirect(url_for('dashboard_login'))
    return render_template('dashboard.html')


# Logout
@app.route('/logout')
def logout():
    session.pop('dashboard_access', None)
    return redirect(url_for('index'))


# Scan QR code - AUTO GATE ASSIGNMENT (NO MANUAL SELECTION)
@app.route('/scan', methods=['POST'])
def scan():
    try:
        qr_data = request.json.get('qr_data')

        data = json.loads(qr_data)
        family_id = data['family_id']

        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()

        # Check last scan to determine entry or exit
        c.execute('''SELECT scan_type FROM scans 
                     WHERE family_id=? 
                     ORDER BY id DESC LIMIT 1''', (family_id,))
        last_scan = c.fetchone()

        # Calculate number of people
        num_people = 0
        if 'student1' in data and data['student1']:
            num_people += 1
        if 'student2' in data and data['student2']:
            num_people += 1
        if 'parents' in data and data['parents']:
            num_people += len(data['parents'])

        # Auto-determine entry/exit and assign gate
        if not last_scan or last_scan[0] == 'exit':
            # First scan or last was exit → This is ENTRY
            scan_type = 'entry'
            gate = '1'  # Entry = Gate 1 (Front Gate)
            message_en = f"✅ Entry Allowed - Gate 1 ({num_people} persons)"
            message_hi = f"✅ प्रवेश की अनुमति - गेट 1 ({num_people} व्यक्ति)"
        else:
            # Last was entry → This is EXIT
            scan_type = 'exit'
            gate = '2'  # Exit = Gate 2 (Side Gate)
            message_en = f"👋 Exit Recorded - Gate 2 ({num_people} persons)"
            message_hi = f"👋 बाहर जाने की अनुमति - गेट 2 ({num_people} व्यक्ति)"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store scan
        c.execute('''INSERT INTO scans VALUES (NULL, ?, ?, ?, ?, ?)''',
                  (family_id, scan_type, timestamp, gate, num_people))
        conn.commit()

        # Calculate totals
        c.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN scan_type='entry' THEN person_count ELSE 0 END), 0),
                COALESCE(SUM(CASE WHEN scan_type='exit' THEN person_count ELSE 0 END), 0)
            FROM scans
        """)
        result = c.fetchone()
        total_entries = result[0] if result[0] else 0
        total_exits = result[1] if result[1] else 0

        conn.close()

        return jsonify({
            'success': True,
            'family': data,
            'scan_type': scan_type,
            'gate': gate,
            'message_en': message_en,
            'message_hi': message_hi,
            'current_count': total_entries - total_exits,
            'total_entries': total_entries,
            'total_exits': total_exits,
            'persons_in_family': num_people,
            'timestamp': timestamp
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# Get stats
@app.route('/api/stats')
def get_stats():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    c.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN scan_type='entry' THEN person_count ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN scan_type='exit' THEN person_count ELSE 0 END), 0)
        FROM scans
    """)
    result = c.fetchone()
    entries = result[0] if result[0] else 0
    exits = result[1] if result[1] else 0

    c.execute('''SELECT s.family_id, s.scan_type, s.timestamp, s.gate_number,
                        f.student1_name, f.class, f.section, s.person_count
                 FROM scans s
                 LEFT JOIN families f ON s.family_id = f.family_id
                 ORDER BY s.id DESC LIMIT 10''')
    recent = [{'family_id': r[0], 'type': r[1], 'time': r[2],
               'gate': r[3], 'student': r[4], 'class': f"{r[5]}-{r[6]}" if r[5] and r[6] else 'N/A',
               'persons': r[7] if len(r) > 7 and r[7] else 1}
              for r in c.fetchall()]

    conn.close()

    return jsonify({
        'total_entries': entries,
        'total_exits': exits,
        'current_inside': entries - exits,
        'recent_scans': recent
    })


# Clear data
@app.route('/api/reset', methods=['POST'])
def reset():
    if not session.get('dashboard_access'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("DELETE FROM scans")
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'All scans cleared'})


if __name__ == '__main__':
    init_db()
    load_sample_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)