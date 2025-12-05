#SOLO RESETEAR IDS GENERAL

import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("=== RESETEAR IDs DE TABLAS ===\n")

# 1. Contar registros actuales
cursor.execute('SELECT COUNT(*) FROM asignaciones')
total_asignaciones = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM auditoria')
total_auditoria = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM actividades_peritos')
total_actividades = cursor.fetchone()[0]

print(f"📊 Registros actuales:")
print(f"   - Asignaciones: {total_asignaciones}")
print(f"   - Auditoría: {total_auditoria}")
print(f"   - Actividades: {total_actividades}")
print()

respuesta = input("⚠️  ¿Deseas resetear los IDs? Esto NO borra datos, solo renumera. (si/no): ")

if respuesta.lower() != 'si':
    print("❌ Cancelado")
    conn.close()
    exit()

print("\n🔄 Reseteando IDs...\n")

# ==================== ASIGNACIONES ====================
print("1️⃣  Reseteando IDs de asignaciones...")

# Obtener todos los registros ordenados por fecha
cursor.execute('SELECT * FROM asignaciones ORDER BY fecha_registro ASC')
asignaciones = cursor.fetchall()

# Crear tabla temporal
cursor.execute('DROP TABLE IF EXISTS asignaciones_temp')
cursor.execute('''
    CREATE TABLE asignaciones_temp AS 
    SELECT * FROM asignaciones WHERE 0
''')

# Insertar con IDs nuevos (empezando desde 1)
for i, row in enumerate(asignaciones, start=1):
    cursor.execute('''
        INSERT INTO asignaciones_temp 
        SELECT * FROM asignaciones WHERE id = ?
    ''', (row[0],))
    
    # Actualizar el ID
    cursor.execute('UPDATE asignaciones_temp SET id = ? WHERE id = ?', (i, row[0]))

# Reemplazar tabla original
cursor.execute('DROP TABLE asignaciones')
cursor.execute('ALTER TABLE asignaciones_temp RENAME TO asignaciones')

# Resetear el contador de SQLite
cursor.execute('DELETE FROM sqlite_sequence WHERE name="asignaciones"')
cursor.execute('INSERT INTO sqlite_sequence (name, seq) VALUES ("asignaciones", ?)', (len(asignaciones),))

print(f"   ✅ {len(asignaciones)} asignaciones renumeradas (1-{len(asignaciones)})")

# ==================== AUDITORÍA ====================
print("2️⃣  Reseteando IDs de auditoría...")

cursor.execute('SELECT * FROM auditoria ORDER BY fecha ASC')
auditorias = cursor.fetchall()

cursor.execute('DROP TABLE IF EXISTS auditoria_temp')
cursor.execute('CREATE TABLE auditoria_temp AS SELECT * FROM auditoria WHERE 0')

for i, row in enumerate(auditorias, start=1):
    cursor.execute('INSERT INTO auditoria_temp SELECT * FROM auditoria WHERE id = ?', (row[0],))
    cursor.execute('UPDATE auditoria_temp SET id = ? WHERE id = ?', (i, row[0]))

cursor.execute('DROP TABLE auditoria')
cursor.execute('ALTER TABLE auditoria_temp RENAME TO auditoria')
cursor.execute('DELETE FROM sqlite_sequence WHERE name="auditoria"')
cursor.execute('INSERT INTO sqlite_sequence (name, seq) VALUES ("auditoria", ?)', (len(auditorias),))

print(f"   ✅ {len(auditorias)} registros de auditoría renumerados (1-{len(auditorias)})")

# ==================== ACTIVIDADES ====================
print("3️⃣  Reseteando IDs de actividades...")

cursor.execute('SELECT * FROM actividades_peritos ORDER BY fecha_registro ASC')
actividades = cursor.fetchall()

cursor.execute('DROP TABLE IF EXISTS actividades_peritos_temp')
cursor.execute('CREATE TABLE actividades_peritos_temp AS SELECT * FROM actividades_peritos WHERE 0')

for i, row in enumerate(actividades, start=1):
    cursor.execute('INSERT INTO actividades_peritos_temp SELECT * FROM actividades_peritos WHERE id = ?', (row[0],))
    cursor.execute('UPDATE actividades_peritos_temp SET id = ? WHERE id = ?', (i, row[0]))

cursor.execute('DROP TABLE actividades_peritos')
cursor.execute('ALTER TABLE actividades_peritos_temp RENAME TO actividades_peritos')
cursor.execute('DELETE FROM sqlite_sequence WHERE name="actividades_peritos"')
cursor.execute('INSERT INTO sqlite_sequence (name, seq) VALUES ("actividades_peritos", ?)', (len(actividades),))

print(f"   ✅ {len(actividades)} actividades renumeradas (1-{len(actividades)})")

conn.commit()
conn.close()

print("\n✅ ¡IDs reseteados exitosamente!")
print("📋 Todos los datos se mantienen, solo cambiaron los números de ID.")