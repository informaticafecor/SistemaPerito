import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

perito_id = 11

print(f"🗑️ Eliminando perito ID {perito_id}...")

# Eliminar todo relacionado
cursor.execute('DELETE FROM asignaciones WHERE perito_id = ?', (perito_id,))
print(f"   ✅ Asignaciones eliminadas")

cursor.execute('DELETE FROM actividades_peritos WHERE perito_id = ?', (perito_id,))
print(f"   ✅ Actividades eliminadas")

cursor.execute('DELETE FROM vacaciones WHERE perito_id = ?', (perito_id,))
print(f"   ✅ Vacaciones eliminadas")

cursor.execute('DELETE FROM usuarios WHERE perito_id = ?', (perito_id,))
print(f"   ✅ Usuario eliminado")

cursor.execute('DELETE FROM peritos WHERE id = ?', (perito_id,))
print(f"   ✅ Perito eliminado")

conn.commit()
conn.close()

print(f"\n✅ Perito ID {perito_id} eliminado completamente de la BD")