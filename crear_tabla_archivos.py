import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Crear tabla de archivos de asignaciones
cursor.execute('''
    CREATE TABLE IF NOT EXISTS archivos_asignaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asignacion_id INTEGER NOT NULL,
        nombre_original TEXT NOT NULL,
        nombre_guardado TEXT NOT NULL,
        tamano INTEGER,
        extension TEXT,
        fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        usuario_id INTEGER,
        usuario_nombre TEXT,
        FOREIGN KEY (asignacion_id) REFERENCES asignaciones(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
''')

conn.commit()
conn.close()

print("✅ Tabla 'archivos_asignaciones' creada exitosamente")