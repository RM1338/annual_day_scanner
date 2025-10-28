import sqlite3

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Check if person_count column exists
c.execute("PRAGMA table_info(scans)")
columns = [row[1] for row in c.fetchall()]

if 'person_count' not in columns:
    print("🔧 Adding person_count column to database...")
    try:
        c.execute("ALTER TABLE scans ADD COLUMN person_count INTEGER DEFAULT 1")
        conn.commit()
        print("✅ Database updated successfully!")
        print("📊 Now scans will count individual persons, not families!")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("✅ Database already has person_count column")
    print("✅ No changes needed!")

conn.close()

print("\n🎉 You can now run your app!")
print("   python app.py")