import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("📊 VERIFICACIÓN DE IDs:\n")

tablas = ['asignaciones', 'auditoria', 'actividades_peritos', 'usuarios', 'vacaciones']

for tabla in tablas:
    cursor.execute(f'SELECT COUNT(*) FROM {tabla} WHERE id IS NULL')
    nulls = cursor.fetchone()[0]
    
    cursor.execute(f'SELECT MIN(id), MAX(id), COUNT(*) FROM {tabla}')
    min_id, max_id, total = cursor.fetchone()
    
    status = "✅" if nulls == 0 else "❌"
    
    print(f"{status} {tabla}:")
    print(f"      IDs NULL: {nulls}")
    print(f"      Rango: {min_id} - {max_id}")
    print(f"      Total: {total}\n")

conn.close()