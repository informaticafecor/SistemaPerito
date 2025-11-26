import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Verificar estructura de la tabla
cursor.execute("PRAGMA table_info(actividades_peritos)")
columnas = cursor.fetchall()

print("=== COLUMNAS ACTUALES ===")
for col in columnas:
    print(f"{col[1]} - {col[2]}")

# Verificar si existe la columna 'estado'
columnas_nombres = [col[1] for col in columnas]

if 'estado' not in columnas_nombres:
    print("\n⚠️ Columna 'estado' NO existe. Agregando...")
    try:
        cursor.execute("ALTER TABLE actividades_peritos ADD COLUMN estado TEXT DEFAULT 'Pendiente'")
        conn.commit()
        print("✅ Columna 'estado' agregada exitosamente")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("\n✅ Columna 'estado' ya existe")

conn.close()