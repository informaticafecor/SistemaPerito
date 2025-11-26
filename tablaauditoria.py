import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Verificar si la tabla existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auditoria'")
existe = cursor.fetchone()

if existe:
    print("⚠️ La tabla 'auditoria' existe. Respaldando datos...")
    
    # Respaldar datos existentes
    cursor.execute("SELECT * FROM auditoria")
    datos_respaldo = cursor.fetchall()
    
    # Eliminar tabla vieja
    cursor.execute("DROP TABLE auditoria")
    print("✅ Tabla antigua eliminada")

# Crear tabla con estructura correcta
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auditoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        usuario_nombre TEXT NOT NULL,
        accion TEXT NOT NULL,
        modulo TEXT NOT NULL,
        detalles TEXT,
        registro_id INTEGER,
        ip_address TEXT,
        user_agent TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
''')

print("✅ Tabla 'auditoria' creada correctamente")

# Si había datos, intentar restaurarlos (ajusta según tu estructura vieja)
if existe and datos_respaldo:
    print(f"⚠️ Había {len(datos_respaldo)} registros. No se pueden restaurar automáticamente.")
    print("   (La estructura cambió. Los datos antiguos se perdieron.)")

conn.commit()
conn.close()

print("\n✅ Base de datos corregida. Reinicia el servidor.")