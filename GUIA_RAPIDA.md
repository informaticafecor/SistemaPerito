# 🚀 GUÍA DE INICIO RÁPIDO - SistemaPerito

Esta guía te ayudará a poner en funcionamiento el sistema en **menos de 5 minutos**.

---

## ⚡ Inicio Rápido (3 Pasos)

### 1️⃣ Preparar el Entorno

Abre **CMD** o **Terminal** en la carpeta del proyecto y ejecuta:
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

Verás `(venv)` al inicio de tu línea de comandos. ✅

### 2️⃣ Instalar Dependencias
```bash
pip install flask openpyxl reportlab
```

Espera unos segundos mientras se instalan los paquetes... ⏳

### 3️⃣ Ejecutar el Sistema
```bash
python app.py
```

Verás este mensaje:
```
============================================================
🚀 SISTEMA PERITO - Iniciado
============================================================
📍 URL: http://127.0.0.1:5000
============================================================
```

**¡LISTO!** Abre tu navegador en: **http://127.0.0.1:5000** 🎉

---

## 📝 Primeros Pasos en el Sistema

### ✅ 1. Verificar que Todo Funciona

1. Abre el navegador en `http://127.0.0.1:5000`
2. Deberías ver el **Dashboard** con:
   - 4 tarjetas de estadísticas (todas en 0)
   - 3 botones de acciones rápidas
   - Tabla vacía de asignaciones
3. El menú superior debe tener 6 opciones

✅ **Si ves esto, ¡todo está funcionando!**

### ✅ 2. Crear Tu Primera Asignación

1. **Clic en "Nueva Asignación"** en el menú
2. Llena el formulario:
```
   Tipo de Perito: Acústico
   Perito: WILBER PAUL ESPINOZA LAUREANO
   Fecha Inicio: (hoy)
   Fecha Fin: (mañana)
```
3. **Clic en "Guardar Asignación"**
4. Verás un mensaje de éxito ✅

### ✅ 3. Ver la Asignación Creada

1. **Vuelve al Dashboard** (clic en "Dashboard")
2. Verás:
   - Total Asignaciones: **1**
   - Pendientes: **1**
   - Tu asignación en la tabla

### ✅ 4. Explorar las Demás Funciones

- **Buscar**: Encuentra asignaciones
- **Calendario**: Vista mensual
- **Peritos**: Lista de 11 peritos
- **Reportes**: Gráficos (tendrás datos después de crear más asignaciones)

---

## 🎯 Casos de Uso Comunes

### 📌 Caso 1: Verificar Disponibilidad de un Perito

**Escenario**: Necesitas asignar a WILBER del 10/12 al 13/12, pero quieres ver si está libre.

**Pasos**:
1. Ve a **Nueva Asignación**
2. Selecciona **Tipo: Acústico**
3. Selecciona **WILBER PAUL ESPINOZA LAUREANO**
4. Ingresa fechas: **10/12/2025** al **13/12/2025**
5. El sistema te dirá automáticamente si está disponible ✅ o no ❌

### 📌 Caso 2: Buscar Todas las Asignaciones de un Perito

**Escenario**: Quieres ver todas las asignaciones de MARCIAL.

**Pasos**:
1. Ve a **Peritos**
2. Busca a **MARCIAL SULCA CAHUANA**
3. Clic en **"Historial"**
4. Verás todas sus asignaciones

### 📌 Caso 3: Exportar Asignaciones del Mes

**Escenario**: Necesitas un Excel con todas las asignaciones de diciembre.

**Pasos**:
1. Ve a **Buscar**
2. Configura:
   - Fecha Desde: **01/12/2025**
   - Fecha Hasta: **31/12/2025**
3. Clic en **"Exportar a Excel"**
4. Se descargará automáticamente 📥

### 📌 Caso 4: Ver Calendario de un Perito Específico

**Escenario**: Quieres ver el calendario solo de ALBERTO.

**Pasos**:
1. Ve a **Calendario**
2. En **"Filtrar por Perito"** selecciona **ALBERTO HONORATO BLACIDO QUITO**
3. Verás solo sus asignaciones marcadas en el calendario

---

## 🔄 Rutina Diaria Recomendada

### Por la Mañana:
1. Abre el sistema
2. Revisa el **Dashboard** → Asignaciones pendientes
3. Ve al **Calendario** → Asignaciones de hoy

### Al Registrar una Asignación:
1. **Nueva Asignación**
2. Llena todos los campos
3. Verifica disponibilidad (el sistema lo hace solo)
4. Guarda

### Por la Tarde:
1. Actualiza estados de asignaciones completadas
2. Revisa el **Calendario** → Asignaciones de mañana

### Al Final del Mes:
1. Ve a **Reportes**
2. Genera estadísticas del mes
3. Exporta a Excel para archivo

---

## 🐛 Soluciones Rápidas

### ❌ No se abre el navegador automáticamente

**Solución**: Abre manualmente `http://127.0.0.1:5000`

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"

**Solución**:
```bash
# Verifica que el entorno virtual esté activado (debe aparecer (venv))
# Si no está activado:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstala:
pip install flask openpyxl reportlab
```

### ❌ Error: "Address already in use"

**Solución**: El puerto 5000 está ocupado.
```bash
# Opción 1: Cierra otros programas que usen el puerto
# Opción 2: Cambia el puerto en app.py línea final:
app.run(debug=True, host='127.0.0.1', port=5001)  # Cambiar a 5001
```

### ❌ La página se ve sin estilos

**Solución**: 
- Verifica tu conexión a internet (usa CDN de TailwindCSS)
- Actualiza la página (Ctrl + F5)

### ❌ No aparecen los peritos

**Solución**:
```bash
# Elimina la base de datos y reinicia
del database.db  # Windows
rm database.db   # Linux/Mac

# Reinicia la aplicación
python app.py
```

---

## 📊 Datos de Ejemplo para Pruebas

Si quieres probar el sistema rápidamente, crea estas asignaciones:

### Asignación 1:
```
Hoja Envío: 000241-2025
Expediente: FPCECC20250000293
Tipo Perito: Acústico
Perito: WILBER PAUL ESPINOZA LAUREANO
Fecha Inicio: 10/12/2025
Fecha Fin: 13/12/2025
Lugar: Lima-Huánuco-Lima
Observaciones: TOMA DE MUESTRA DE VOZ
```

### Asignación 2:
```
Tipo Perito: Informático
Perito: ALBERTO HONORATO BLACIDO QUITO
Fecha Inicio: 15/12/2025
Fecha Fin: 16/12/2025
Observaciones: Análisis de dispositivos móviles
```

### Asignación 3:
```
Tipo Perito: Contable
Perito: ROSARIO CORDERO BORJA
Fecha Inicio: 18/12/2025
Fecha Fin: 20/12/2025
Observaciones: Pericia contable sobre ingresos y egresos
```

Después de crear estas 3, explora:
- **Dashboard**: Verás las estadísticas
- **Calendario**: Verás los eventos marcados
- **Reportes**: Verás los gráficos con datos

---

## 🎓 Tips para Usuarios Nuevos

### ✅ Tip 1: Usa el Sistema de Validación
El sistema verifica automáticamente si un perito está disponible. Confía en las alertas.

### ✅ Tip 2: Exporta Regularmente
Exporta tus datos a Excel cada semana para tener respaldos.

### ✅ Tip 3: Usa el Calendario
El calendario es la mejor forma de visualizar la carga de trabajo.

### ✅ Tip 4: Aprovecha los Filtros
En búsqueda y calendario, usa los filtros para encontrar información rápidamente.

### ✅ Tip 5: Revisa los Reportes
Los reportes te ayudan a identificar patrones y optimizar asignaciones.

---

## 📱 Atajos de Teclado (Próximamente)

Actualmente no hay atajos de teclado, pero próximamente:
- `Ctrl + N`: Nueva asignación
- `Ctrl + F`: Buscar
- `Ctrl + K`: Calendario
- `Esc`: Cerrar modales

---

## 🔒 Backup de Datos

### Hacer Backup Manual:

**Windows**:
```bash
copy database.db backup\database_2025-12-15.db
```

**Linux/Mac**:
```bash
cp database.db backup/database_2025-12-15.db
```

### Restaurar Backup:

**Windows**:
```bash
copy backup\database_2025-12-15.db database.db
```

**Linux/Mac**:
```bash
cp backup/database_2025-12-15.db database.db
```

---

## 📞 ¿Necesitas Ayuda?

1. ✅ Revisa esta guía
2. ✅ Lee el `README.md` completo
3. ✅ Revisa la sección "Solución de Problemas"
4. ✅ Verifica que todo esté instalado correctamente

---

## 🎉 ¡Felicitaciones!

Ya sabes usar **SistemaPerito**. Ahora:

1. ✅ Crea tus primeras asignaciones
2. ✅ Explora todas las funciones
3. ✅ Personaliza según tus necesidades
4. ✅ Disfruta de una gestión eficiente

**¡Éxito con tu sistema!** 🚀