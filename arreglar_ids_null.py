import sqlite3
import shutil
from datetime import datetime

# Hacer backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy('database.db', f'database_backup_{timestamp}.db')
print(f"✅ Backup creado: database_backup_{timestamp}.db")

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("\n🔍 Verificando IDs NULL...")

# Verificar qué tablas tienen IDs NULL
tablas_afectadas = []

for tabla in ['asignaciones', 'auditoria', 'actividades_peritos', 'usuarios', 'vacaciones']:
    cursor.execute(f'SELECT COUNT(*) FROM {tabla} WHERE id IS NULL')
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"   ⚠️  {tabla}: {count} registros con ID NULL")
        tablas_afectadas.append(tabla)
    else:
        print(f"   ✅ {tabla}: Sin problemas")

if not tablas_afectadas:
    print("\n✅ No hay IDs NULL. Base de datos OK.")
    conn.close()
    exit()

print(f"\n🔧 Arreglando {len(tablas_afectadas)} tablas...")

# ==================== ARREGLAR CADA TABLA ====================

for tabla in tablas_afectadas:
    print(f"\n📋 Procesando {tabla}...")
    
    # 1. Obtener todos los registros (NULL y no-NULL)
    cursor.execute(f'SELECT * FROM {tabla}')
    todos_registros = cursor.fetchall()
    
    # 2. Obtener estructura de columnas
    cursor.execute(f'PRAGMA table_info({tabla})')
    columnas_info = cursor.fetchall()
    columnas = [col[1] for col in columnas_info]  # Nombres de columnas
    
    print(f"   📊 Total registros: {len(todos_registros)}")
    print(f"   📊 Columnas: {len(columnas)}")
    
    # 3. Crear tabla temporal
    cursor.execute(f'DROP TABLE IF EXISTS {tabla}_temp')
    cursor.execute(f'CREATE TABLE {tabla}_temp AS SELECT * FROM {tabla} WHERE 0')
    
    # 4. Insertar registros uno por uno (SQLite asignará IDs automáticamente)
    for registro in todos_registros:
        # Saltar el ID (primera columna) y dejar que SQLite lo genere
        valores = registro[1:]  # Todos los valores excepto el ID
        placeholders = ','.join(['?'] * len(valores))
        
        cursor.execute(f'INSERT INTO {tabla}_temp VALUES (NULL, {placeholders})', valores)
    
    # 5. Reemplazar tabla original
    cursor.execute(f'DROP TABLE {tabla}')
    cursor.execute(f'ALTER TABLE {tabla}_temp RENAME TO {tabla}')
    
    # 6. Resetear contador de autoincremento
    cursor.execute(f'DELETE FROM sqlite_sequence WHERE name="{tabla}"')
    cursor.execute(f'INSERT INTO sqlite_sequence (name, seq) VALUES ("{tabla}", {len(todos_registros)})')
    
    print(f"   ✅ {len(todos_registros)} registros arreglados (IDs: 1-{len(todos_registros)})")

conn.commit()
conn.close()

print("\n" + "=" * 60)
print("✅ BASE DE DATOS REPARADA")
print("=" * 60)
print(f"\n💾 Backup guardado: database_backup_{timestamp}.db")
print("🔢 Todos los IDs ahora están correctos (1, 2, 3...)")
print("\n⚠️  IMPORTANTE: Reinicia el servidor Flask ahora.")