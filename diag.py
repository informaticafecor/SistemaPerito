import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM auditoria ORDER BY fecha DESC LIMIT 10')
registros = cursor.fetchall()

print("=== ÚLTIMOS 10 REGISTROS ===")
for reg in registros:
    print(reg)

conn.close()