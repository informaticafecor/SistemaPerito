import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("=== LIMPIEZA DE BASE DE DATOS ===\n")

# 1. Mostrar estadísticas actuales
cursor.execute('SELECT COUNT(*) FROM asignaciones')
total_asignaciones = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM actividades_peritos')
total_actividades = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM vacaciones')
total_vacaciones = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM usuarios WHERE usuario != "admin"')
total_usuarios = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM peritos')
total_peritos = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM auditoria')
total_auditoria = cursor.fetchone()[0]

print(f"📊 REGISTROS ACTUALES:")
print(f"   - Asignaciones: {total_asignaciones}")
print(f"   - Actividades: {total_actividades}")
print(f"   - Vacaciones: {total_vacaciones}")
print(f"   - Usuarios (sin admin): {total_usuarios}")
print(f"   - Peritos: {total_peritos}")
print(f"   - Auditoría: {total_auditoria}")
print()

# 2. Preguntar qué limpiar
print("¿Qué deseas limpiar?")
print("1. Asignaciones")
print("2. Actividades de peritos")
print("3. Vacaciones")
print("4. Usuarios (excepto admin)")
print("5. Peritos (y sus asignaciones/actividades)")
print("6. Auditoría")
print("7. TODO (excepto admin y tabla de peritos)")
print("8. Cancelar")
print()

opcion = input("Ingresa el número de opción: ")

if opcion == '1':
    cursor.execute('DELETE FROM asignaciones')
    cursor.execute('DELETE FROM archivos_asignaciones')
    print("✅ Asignaciones eliminadas")

elif opcion == '2':
    cursor.execute('DELETE FROM actividades_peritos')
    print("✅ Actividades eliminadas")

elif opcion == '3':
    cursor.execute('DELETE FROM vacaciones')
    print("✅ Vacaciones eliminadas")

elif opcion == '4':
    cursor.execute('DELETE FROM usuarios WHERE usuario != "admin"')
    print("✅ Usuarios eliminados (admin preservado)")

elif opcion == '5':
    # Mostrar peritos
    cursor.execute('SELECT id, nombre_completo, tipo FROM peritos')
    peritos = cursor.fetchall()
    print("\n📋 PERITOS ACTUALES:")
    for p in peritos:
        print(f"   {p[0]}. {p[1]} ({p[2]})")
    
    perito_id = input("\nIngresa el ID del perito a eliminar (o 'todos' para eliminar todos): ")
    
    if perito_id.lower() == 'todos':
        cursor.execute('DELETE FROM asignaciones')
        cursor.execute('DELETE FROM actividades_peritos')
        cursor.execute('DELETE FROM vacaciones')
        cursor.execute('DELETE FROM usuarios WHERE rol = "perito"')
        cursor.execute('DELETE FROM peritos')
        print("✅ Todos los peritos y sus registros eliminados")
    else:
        cursor.execute('DELETE FROM asignaciones WHERE perito_id = ?', (perito_id,))
        cursor.execute('DELETE FROM actividades_peritos WHERE perito_id = ?', (perito_id,))
        cursor.execute('DELETE FROM vacaciones WHERE perito_id = ?', (perito_id,))
        cursor.execute('DELETE FROM usuarios WHERE perito_id = ?', (perito_id,))
        cursor.execute('DELETE FROM peritos WHERE id = ?', (perito_id,))
        print(f"✅ Perito ID {perito_id} y sus registros eliminados")

elif opcion == '6':
    cursor.execute('DELETE FROM auditoria')
    print("✅ Auditoría eliminada")

elif opcion == '7':
    cursor.execute('DELETE FROM asignaciones')
    cursor.execute('DELETE FROM archivos_asignaciones')
    cursor.execute('DELETE FROM actividades_peritos')
    cursor.execute('DELETE FROM vacaciones')
    cursor.execute('DELETE FROM auditoria')
    cursor.execute('DELETE FROM historial')
    cursor.execute('DELETE FROM usuarios WHERE usuario != "admin"')
    print("✅ TODO eliminado (excepto admin y peritos)")

elif opcion == '8':
    print("❌ Cancelado")
    conn.close()
    exit()

else:
    print("❌ Opción inválida")
    conn.close()
    exit()

# Confirmar cambios
conn.commit()
conn.close()

print("\n✅ Limpieza completada exitosamente")