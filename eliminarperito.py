import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Mostrar peritos
cursor.execute('SELECT id, nombre_completo, tipo FROM peritos')
print("PERITOS:")
for p in cursor.fetchall():
    print(f"ID {p[0]}: {p[1]} ({p[2]})")

# Eliminar
perito_id = input("\nID del perito a eliminar: ")

cursor.execute('DELETE FROM asignaciones WHERE perito_id = ?', (perito_id,))
cursor.execute('DELETE FROM actividades_peritos WHERE perito_id = ?', (perito_id,))
cursor.execute('DELETE FROM vacaciones WHERE perito_id = ?', (perito_id,))
cursor.execute('DELETE FROM usuarios WHERE perito_id = ?', (perito_id,))
cursor.execute('DELETE FROM peritos WHERE id = ?', (perito_id,))

conn.commit()
conn.close()

print(f"✅ Perito {perito_id} eliminado completamente")