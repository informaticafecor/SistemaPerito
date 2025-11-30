import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Verificar roles existentes
cursor.execute("SELECT DISTINCT rol FROM usuarios")
roles = cursor.fetchall()
print("Roles actuales:", roles)

# No necesitamos cambiar nada en la tabla, solo usar 'invitado' como nuevo rol

conn.close()
print("✅ Listo para usar rol 'invitado'")