2. Descartar tus cambios (si NO te importan y quieres reemplazar todo con lo del servidor)

⚠️ CUIDADO, esto borrará tus cambios locales.

git reset --hard
git pull



import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Agregar columna estado si no existe
try:
    cursor.execute("ALTER TABLE actividades_peritos ADD COLUMN estado TEXT DEFAULT 'Pendiente'")
    conn.commit()
    print("✅ Columna 'estado' agregada exitosamente")
except sqlite3.OperationalError as e:
    print("⚠️ La columna ya existe o hubo un error:", e)

conn.close()


🔧 VERIFICAR QUE LA COLUMNA estado EXISTE
Ejecuta este script para verificar/agregar la columna:
pythonimport sqlite3

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





📋 PASO 1: Verificar que la tabla de auditoría existe y tiene todos los campos
Ejecuta este script para verificar/crear la tabla:
pythonimport sqlite3

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



import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Ver estructura actual
cursor.execute("PRAGMA table_info(auditoria)")
columnas = cursor.fetchall()

print("=== COLUMNAS ACTUALES DE AUDITORÍA ===")
for col in columnas:
    print(f"{col[1]} ({col[2]})")

conn.close()






 PASO 2: Recrear la tabla de auditoría correctamente
Ejecuta este script para corregir la tabla:
pythonimport sqlite3

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











📋 OTRAS MEJORAS RECOMENDADAS
1. Agregar índices a la tabla de auditoría (para búsquedas rápidas)
pythonimport sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Crear índices
cursor.execute('CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON auditoria(usuario_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha_hora)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_auditoria_accion ON auditoria(accion)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_auditoria_modulo ON auditoria(modulo)')

conn.commit()
conn.close()

print("✅ Índices creados para búsquedas rápidas")




PASO 1: Verificar estructura actual
Ejecuta esto para ver exactamente qué columnas tienes:
pythonimport sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(auditoria)")
columnas = cursor.fetchall()

print("=== COLUMNAS ACTUALES ===")
for col in columnas:
    print(f"{col[1]} ({col[2]})")

conn.close()


import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE asignaciones ADD COLUMN denominacion TEXT")
    conn.commit()
    print("✅ Columna 'denominacion' agregada")
except sqlite3.OperationalError as e:
    print("⚠️ La columna ya existe o error:", e)

conn.close()


PASO 2: Ejecutar script para crear la tabla
Crea un archivo crear_tabla_archivos.py:
pythonimport sqlite3

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


👤 CREAR NUEVO ROL: "INVITADO" (solo Dashboard y Calendario)
PASO 1: Actualizar tabla de usuarios
Ejecuta este script:
pythonimport sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Verificar roles existentes
cursor.execute("SELECT DISTINCT rol FROM usuarios")
roles = cursor.fetchall()
print("Roles actuales:", roles)

# No necesitamos cambiar nada en la tabla, solo usar 'invitado' como nuevo rol

conn.close()
print("✅ Listo para usar rol 'invitado'")





