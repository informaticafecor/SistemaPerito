import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE asignaciones ADD COLUMN denominacion TEXT")
    conn.commit()
    print("✅ Columna 'denominacion' agregada")
except sqlite3.OperationalError as e:
    print("⚠️ La columna ya existe o error:", e)

conn.close()