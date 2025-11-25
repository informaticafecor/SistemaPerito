import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Buscar el usuario
cursor.execute('''
    SELECT u.id, u.usuario, u.rol, u.perito_id, p.nombre_completo, p.tipo
    FROM usuarios u
    LEFT JOIN peritos p ON u.perito_id = p.id
    WHERE p.nombre_completo LIKE '%WILBER PAUL%'
''')

result = cursor.fetchone()
if result:
    print(f"Usuario ID: {result[0]}")
    print(f"Username: {result[1]}")
    print(f"Rol: {result[2]}")
    print(f"Perito ID: {result[3]}")
    print(f"Nombre Perito: {result[4]}")
    print(f"Tipo: {result[5]}")
else:
    print("Usuario no encontrado")

conn.close()