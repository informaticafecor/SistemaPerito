import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Verificar permisos del usuario 10
cursor.execute('SELECT * FROM usuarios WHERE id = 10')
user = cursor.fetchone()
print("Usuario:", user)

# Verificar actividades del perito 6
cursor.execute('SELECT id, perito_id FROM actividades_peritos WHERE perito_id = 6')
acts = cursor.fetchall()
print("Actividades:", acts)

conn.close()