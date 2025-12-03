import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Ver peritos actuales
cursor.execute('SELECT id, nombre_completo, tipo FROM peritos')
print("=== PERITOS ACTUALES ===")
for p in cursor.fetchall():
    print(f"ID {p[0]}: {p[1]} ({p[2]})")

print()

# Actualizar
perito_id = input("ID del perito a actualizar: ")
nuevo_nombre = input("Nuevo nombre completo: ")

cursor.execute('UPDATE peritos SET nombre_completo = ? WHERE id = ?', (nuevo_nombre, perito_id))

conn.commit()
conn.close()

print(f"\n✅ Perito ID {perito_id} actualizado a: {nuevo_nombre}")