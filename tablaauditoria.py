import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Crear tabla de auditoría si no existe
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

# Verificar columnas
cursor.execute("PRAGMA table_info(auditoria)")
columnas = cursor.fetchall()

print("=== COLUMNAS DE AUDITORÍA ===")
for col in columnas:
    print(f"{col[1]} - {col[2]}")

# Verificar si faltan columnas y agregarlas
columnas_nombres = [col[1] for col in columnas]

if 'ip_address' not in columnas_nombres:
    cursor.execute("ALTER TABLE auditoria ADD COLUMN ip_address TEXT")
    print("✅ Columna 'ip_address' agregada")

if 'user_agent' not in columnas_nombres:
    cursor.execute("ALTER TABLE auditoria ADD COLUMN user_agent TEXT")
    print("✅ Columna 'user_agent' agregada")

conn.commit()
conn.close()

print("\n✅ Tabla de auditoría lista")