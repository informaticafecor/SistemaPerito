import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Ver todas las actividades del perito 6
cursor.execute('''
    SELECT id, tipo_actividad, fecha_inicio, perito_id
    FROM actividades_peritos 
    WHERE perito_id = 6
''')

print("=== ACTIVIDADES DEL PERITO 6 (WILBER) ===")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Actividad: {row[1]}, Fecha: {row[2]}, Perito ID: {row[3]}")

conn.close()