import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(peritos)")
print(cursor.fetchall())
cursor.execute("SELECT * FROM peritos LIMIT 5")
print(cursor.fetchall())
conn.close()