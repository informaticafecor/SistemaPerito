
✅ 1. NO me importa la versión local de database.db, quiero la del repositorio.
git restore database.db
→ Comando seguro si quieres simplemente obtener lo que está en el repo:

git restore database.db
git pull






# 🗄️ ESTRUCTURA DE BASE DE DATOS - SistemaPerito

Documentación completa de la base de datos SQLite del sistema.






---

## 📊 Diagrama General
```
┌─────────────────┐
│     peritos     │
└─────────────────┘
        │ 1
        │
        │ N
        ▼
┌─────────────────┐      ┌─────────────────┐
│  asignaciones   │──────│   historial     │
└─────────────────┘  1:N └─────────────────┘
```

---

## 📋 Tabla: `peritos`

Almacena la información de todos los peritos del sistema.

### Estructura:

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID único del perito |
| `nombre_completo` | TEXT | NOT NULL | Nombre completo del perito |
| `tipo` | TEXT | NOT NULL | Tipo: Informático, Acústico, Antropólogo, Contable |
| `estado` | TEXT | DEFAULT 'Activo' | Estado: Activo o Inactivo |
| `fecha_creacion` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de registro |

### Datos Iniciales:
```sql
-- 11 peritos precargados al iniciar el sistema

-- Informáticos (3)
1. ALBERTO HONORATO BLACIDO QUITO
2. MISAEL EDSON PALOMINO AYLAS
3. LUIS ALBERTO VILLANUEVA HUAMAN

-- Acústicos (3)
4. MARCIAL SULCA CAHUANA
5. EDILBERTO EDISON ZAVALA CAMPOS
6. WILBER PAUL ESPINOZA LAUREANO

-- Antropólogos (2)
7. BRIAN BARRY SOTO ALCAZAR
8. SANDRA LISBET IBARRA APAZA

-- Contables (3)
9. ROSARIO CORDERO BORJA
10. ANGELA ROXANA CALDERON BUSTAMANTE
11. YESENIA ELIZABETH CHAVEZ VALERO
```

### Ejemplo de Registro:
```sql
{
    "id": 1,
    "nombre_completo": "ALBERTO HONORATO BLACIDO QUITO",
    "tipo": "Informático",
    "estado": "Activo",
    "fecha_creacion": "2025-01-15 10:30:00"
}
```

---

## 📋 Tabla: `asignaciones`

Almacena todas las asignaciones de peritos.

### Estructura:

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID único de la asignación |
| `hoja_envio` | TEXT | NULL | Número de hoja de envío |
| `expediente` | TEXT | NULL | Número de expediente |
| `dependencia` | TEXT | NULL | Dependencia solicitante |
| `tipo_perito` | TEXT | NULL | Tipo de perito requerido |
| `carpeta_fiscal` | TEXT | NULL | Número de carpeta fiscal |
| `observaciones` | TEXT | NULL | Descripción del trabajo/observaciones |
| `lugar` | TEXT | NULL | Lugar del desplazamiento |
| `fecha_inicio` | TEXT | NOT NULL | Fecha de inicio (YYYY-MM-DD) |
| `fecha_fin` | TEXT | NOT NULL | Fecha de fin (YYYY-MM-DD) |
| `perito_asignado` | TEXT | NULL | Nombre del perito (texto libre) |
| `perito_id` | INTEGER | FOREIGN KEY | ID del perito (relación) |
| `desginacion` | TEXT | NULL | Número de designación |
| `oficio_desplazamiento` | TEXT | NULL | Número de oficio de desplazamiento |
| `estado` | TEXT | DEFAULT 'Pendiente' | Pendiente, En Proceso, Completado, Cancelado |
| `fecha_registro` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha y hora de registro |

### Relaciones:
```sql
FOREIGN KEY (perito_id) REFERENCES peritos(id)
```

### Estados Posibles:

1. **Pendiente**: Asignación creada, aún no iniciada
2. **En Proceso**: Perito realizando el trabajo
3. **Completado**: Trabajo finalizado
4. **Cancelado**: Asignación cancelada

### Ejemplo de Registro:
```sql
{
    "id": 1,
    "hoja_envio": "000241-2025",
    "expediente": "FPCECC20250000293",
    "dependencia": "UCAYALI",
    "tipo_perito": "Acústico",
    "carpeta_fiscal": "06-2025",
    "observaciones": "TOMA DE MUESTRA DE VOZ",
    "lugar": "DESPLAZAMIENTO A PASCO - Lima-Huánuco-Lima",
    "fecha_inicio": "2025-12-10",
    "fecha_fin": "2025-12-13",
    "perito_asignado": "WILBER",
    "perito_id": 6,
    "desginacion": "024076-2025 POR DESPACHO",
    "oficio_desplazamiento": "OFICIO 007305-2025-FSCN-FECCO",
    "estado": "Pendiente",
    "fecha_registro": "2025-01-15 10:35:22"
}
```

---

## 📋 Tabla: `historial`

Registra todas las acciones realizadas sobre las asignaciones (auditoría).

### Estructura:

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID único del registro |
| `asignacion_id` | INTEGER | FOREIGN KEY | ID de la asignación relacionada |
| `accion` | TEXT | NOT NULL | Tipo de acción realizada |
| `detalles` | TEXT | NULL | Detalles adicionales |
| `fecha_hora` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha y hora de la acción |

### Relaciones:
```sql
FOREIGN KEY (asignacion_id) REFERENCES asignaciones(id)
```

### Tipos de Acciones:

1. **Creado**: Asignación creada
2. **Modificado**: Asignación actualizada
3. **Completado**: Asignación marcada como completada
4. **Cancelado**: Asignación cancelada

### Ejemplo de Registro:
```sql
{
    "id": 1,
    "asignacion_id": 1,
    "accion": "Creado",
    "detalles": "Asignación creada exitosamente",
    "fecha_hora": "2025-01-15 10:35:22"
}
```

---

## 🔍 Consultas SQL Útiles

### 1. Obtener todas las asignaciones de un perito:
```sql
SELECT a.*, p.nombre_completo
FROM asignaciones a
LEFT JOIN peritos p ON a.perito_id = p.id
WHERE p.id = 6;
```

### 2. Verificar disponibilidad de un perito:
```sql
SELECT * FROM asignaciones
WHERE perito_id = 6
AND estado != 'Cancelado'
AND (
    (fecha_inicio <= '2025-12-13' AND fecha_fin >= '2025-12-10') OR
    (fecha_inicio <= '2025-12-13' AND fecha_fin >= '2025-12-13') OR
    (fecha_inicio >= '2025-12-10' AND fecha_fin <= '2025-12-13')
);
```

### 3. Estadísticas por estado:
```sql
SELECT estado, COUNT(*) as total
FROM asignaciones
GROUP BY estado;
```

### 4. Top 5 peritos con más asignaciones:
```sql
SELECT p.nombre_completo, COUNT(a.id) as total
FROM peritos p
LEFT JOIN asignaciones a ON p.id = a.perito_id
GROUP BY p.id
ORDER BY total DESC
LIMIT 5;
```

### 5. Asignaciones por mes:
```sql
SELECT strftime('%Y-%m', fecha_inicio) as mes, COUNT(*) as total
FROM asignaciones
WHERE fecha_inicio >= date('now', '-6 months')
GROUP BY mes
ORDER BY mes;
```

### 6. Asignaciones de un mes específico:
```sql
SELECT * FROM asignaciones
WHERE fecha_inicio >= '2025-12-01'
AND fecha_fin <= '2025-12-31'
ORDER BY fecha_inicio;
```

---

## 🔐 Índices (Optimización)

Aunque SQLite crea índices automáticamente para PRIMARY KEY y FOREIGN KEY, 
se pueden agregar índices adicionales para mejorar el rendimiento:
```sql
-- Índice para búsquedas por expediente
CREATE INDEX idx_expediente ON asignaciones(expediente);

-- Índice para búsquedas por fechas
CREATE INDEX idx_fechas ON asignaciones(fecha_inicio, fecha_fin);

-- Índice para filtrar por estado
CREATE INDEX idx_estado ON asignaciones(estado);

-- Índice para búsquedas por tipo de perito
CREATE INDEX idx_tipo ON peritos(tipo);
```

---

## 📊 Tamaño de la Base de Datos

### Estimaciones:

- **Base de datos vacía**: ~50 KB
- **Con 100 asignaciones**: ~150 KB
- **Con 1,000 asignaciones**: ~1 MB
- **Con 10,000 asignaciones**: ~8-10 MB

SQLite es muy eficiente y puede manejar millones de registros sin problemas.

---

## 🛠️ Mantenimiento

### Compactar la base de datos:
```sql
VACUUM;
```

Esto elimina espacio no utilizado y reorganiza la base de datos.

### Verificar integridad:
```sql
PRAGMA integrity_check;
```

Verifica que la base de datos no tenga corrupción.

---

## 📝 Migraciones Futuras

Si necesitas agregar campos nuevos:
```sql
-- Ejemplo: Agregar campo de teléfono a peritos
ALTER TABLE peritos ADD COLUMN telefono TEXT;

-- Ejemplo: Agregar campo de prioridad a asignaciones
ALTER TABLE asignaciones ADD COLUMN prioridad TEXT DEFAULT 'Normal';
```

---

**Documentación de Base de Datos Completa ✅**