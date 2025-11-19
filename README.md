# 🏛️ SistemaPerito - Sistema de Gestión de Asignaciones de Peritos

Sistema web profesional para la gestión y control de asignaciones de peritos forenses, desarrollado con Flask, SQLite y TailwindCSS.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionalidades](#funcionalidades)
- [API Endpoints](#api-endpoints)
- [Tecnologías](#tecnologías)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Solución de Problemas](#solución-de-problemas)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## ✨ Características

### 🎯 Funcionalidades Principales

- ✅ **Gestión Completa de Asignaciones**
  - Registro de asignaciones con validación de disponibilidad
  - Verificación automática de conflictos de fechas
  - Estados: Pendiente, En Proceso, Completado, Cancelado

- 👥 **Administración de Peritos**
  - 11 peritos organizados por especialidad
  - 4 tipos: Informático, Acústico, Antropólogo, Contable
  - Historial individual de asignaciones

- 📅 **Calendario Interactivo**
  - Vista mensual con código de colores
  - Filtrado por perito
  - Navegación intuitiva mes a mes

- 🔍 **Búsqueda Avanzada**
  - Búsqueda por múltiples criterios
  - Filtros por estado, tipo, fechas
  - Resultados en tiempo real

- 📊 **Reportes y Estadísticas**
  - Gráficos interactivos (Chart.js)
  - Top 5 peritos más asignados
  - Análisis por dependencia
  - Tendencias mensuales

- 📤 **Exportación de Datos**
  - Exportar a Excel (.xlsx) con formato profesional
  - Exportar a PDF con tablas estructuradas
  - Exportación con filtros aplicados

---

## 🔧 Requisitos Previos

Antes de instalar, asegúrate de tener:

- **Python 3.8 o superior** 
  - Verifica con: `python --version`
  - Descarga desde: [python.org](https://www.python.org/downloads/)

- **pip** (gestor de paquetes de Python)
  - Verifica con: `pip --version`

- **Git** (opcional, para clonar el repositorio)
  - Verifica con: `git --version`

---

## 🚀 Instalación

### Paso 1: Descargar el Proyecto

Opción A - Con Git:
```bash
git clone https://github.com/tuusuario/SistemaPerito.git
cd SistemaPerito
```

Opción B - Sin Git:
1. Descarga todos los archivos del proyecto
2. Colócalos en una carpeta llamada `SistemaPerito`
3. Abre terminal/CMD en esa carpeta

### Paso 2: Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Verás `(venv)` al inicio de tu línea de comandos.

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0
- openpyxl 3.1.2 (para Excel)
- reportlab 4.0.7 (para PDF)
- Werkzeug 3.0.1

### Paso 4: Verificar Instalación
```bash
python app.py
```

Deberías ver:
```
============================================================
🚀 SISTEMA PERITO - Iniciado
============================================================
📍 URL: http://127.0.0.1:5000
📊 Dashboard: http://127.0.0.1:5000
➕ Nueva Asignación: http://127.0.0.1:5000/nuevo
🔍 Búsqueda: http://127.0.0.1:5000/buscar
📅 Calendario: http://127.0.0.1:5000/calendario
👥 Peritos: http://127.0.0.1:5000/peritos
📈 Reportes: http://127.0.0.1:5000/reportes
============================================================
💡 Presiona CTRL+C para detener el servidor
============================================================
```

---

## 🎮 Uso

### Iniciar el Sistema

1. **Activar entorno virtual** (si no está activado):
```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
```

2. **Ejecutar la aplicación**:
```bash
   python app.py
```

3. **Abrir navegador**:
   - Ve a: `http://127.0.0.1:5000`
   - O haz clic en el enlace que aparece en la terminal

### Detener el Sistema

- Presiona `CTRL + C` en la terminal

### Usar el Sistema

#### 📝 Crear Nueva Asignación

1. Ir a **Nueva Asignación** en el menú
2. Llenar el formulario:
   - **Datos del documento**: Hoja de envío, expediente, etc.
   - **Selección de perito**: Tipo y nombre específico
   - **Fechas**: Inicio y fin de la asignación
   - **Ubicación**: Lugar del desplazamiento
3. El sistema validará automáticamente la disponibilidad
4. Guardar la asignación

#### 🔍 Buscar Asignaciones

1. Ir a **Buscar** en el menú
2. Opciones de búsqueda:
   - **Búsqueda general**: Por cualquier término
   - **Filtros**: Estado, tipo de perito, fechas
   - **Campo específico**: Hoja de envío, expediente, etc.
3. Ver resultados en tabla
4. Exportar a Excel si es necesario

#### 📅 Ver Calendario

1. Ir a **Calendario** en el menú
2. Navegar por meses
3. Ver asignaciones por día (código de colores)
4. Filtrar por perito específico
5. Hacer clic en eventos para ver detalles

#### 👥 Gestionar Peritos

1. Ir a **Peritos** en el menú
2. Ver todos los peritos organizados por tipo
3. Opciones:
   - Ver historial de asignaciones
   - Ver calendario individual
   - Filtrar por tipo

#### 📊 Ver Reportes

1. Ir a **Reportes** en el menú
2. Seleccionar período de análisis
3. Ver:
   - Estadísticas generales
   - Gráficos interactivos
   - Top 5 peritos
   - Análisis por dependencia
4. Exportar reporte a Excel

---

## 📁 Estructura del Proyecto
```
SistemaPerito/
│
├── app.py                      # Aplicación principal Flask
├── database.db                 # Base de datos SQLite (se crea automáticamente)
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
│
├── templates/                  # Plantillas HTML
│   ├── index.html             # Dashboard principal
│   ├── nuevo.html             # Formulario de nueva asignación
│   ├── buscar.html            # Búsqueda avanzada
│   ├── calendario.html        # Vista de calendario
│   ├── peritos.html           # Gestión de peritos
│   └── reportes.html          # Reportes y estadísticas
│
├── static/                     # Archivos estáticos
│   ├── css/                   # Estilos personalizados
│   │   └── style.css
│   └── js/                    # Scripts personalizados
│       └── app.js
│
├── exports/                    # Archivos exportados (se crea automáticamente)
│   ├── asignaciones_*.xlsx
│   └── reporte_*.pdf
│
└── venv/                       # Entorno virtual (no subir a Git)
```

---

## 🎯 Funcionalidades

### 1. Dashboard Principal

- **Vista general del sistema**
- Estadísticas en tiempo real
- Últimas 10 asignaciones
- Acciones rápidas

### 2. Nueva Asignación

- **Formulario inteligente** con validación
- Verificación automática de disponibilidad
- Alertas de conflictos de fechas
- Campos autocompletables

### 3. Búsqueda Avanzada

- **Múltiples criterios de búsqueda**
- Filtros combinables
- Resultados instantáneos
- Exportación de resultados

### 4. Calendario

- **Vista mensual interactiva**
- Código de colores por tipo de perito
- Navegación mes a mes
- Detalles de asignaciones por día

### 5. Gestión de Peritos

- **11 peritos predefinidos**:
  - 3 Informáticos
  - 3 Acústicos
  - 2 Antropólogos
  - 3 Contables
- Vista de tarjetas o tabla
- Historial individual
- Estadísticas por perito

### 6. Reportes

- **Gráficos interactivos**:
  - Distribución por estado
  - Distribución por tipo
  - Tendencia mensual
- Top 5 peritos
- Análisis por dependencia
- Exportación a Excel/PDF

---

## 🔌 API Endpoints

### Asignaciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/asignaciones` | Obtener todas las asignaciones |
| GET | `/api/asignacion/<id>` | Obtener asignación específica |
| POST | `/api/asignacion` | Crear nueva asignación |
| PUT | `/api/asignacion/<id>` | Actualizar asignación |
| DELETE | `/api/asignacion/<id>` | Cancelar asignación |

### Peritos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/peritos` | Obtener todos los peritos |

### Validación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/verificar-disponibilidad` | Verificar disponibilidad de perito |

### Búsqueda

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/buscar` | Búsqueda avanzada |

### Estadísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/estadisticas` | Obtener estadísticas generales |

### Exportación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/exportar/excel` | Exportar a Excel |
| GET | `/api/exportar/pdf` | Exportar a PDF |

---

## 🛠️ Tecnologías

### Backend

- **Python 3.8+**: Lenguaje de programación
- **Flask 3.0.0**: Framework web
- **SQLite**: Base de datos
- **openpyxl**: Generación de Excel
- **reportlab**: Generación de PDF

### Frontend

- **HTML5**: Estructura
- **TailwindCSS**: Estilos (vía CDN)
- **JavaScript Vanilla**: Interactividad
- **Font Awesome 6**: Iconos
- **Chart.js**: Gráficos

### Desarrollo

- **Jinja2**: Motor de plantillas
- **SQLite3**: Manejo de base de datos
- **Werkzeug**: Utilidades WSGI

---

## 📸 Capturas de Pantalla

### Dashboard Principal
![Dashboard](docs/screenshots/dashboard.png)

### Nueva Asignación
![Nueva Asignación](docs/screenshots/nuevo.png)

### Calendario
![Calendario](docs/screenshots/calendario.png)

### Reportes
![Reportes](docs/screenshots/reportes.png)

---

## 🐛 Solución de Problemas

### Problema: "python no se reconoce como comando"

**Solución:**
- Asegúrate de tener Python instalado
- Agrega Python al PATH de Windows
- Intenta usar `py` en lugar de `python`

### Problema: "No module named 'flask'"

**Solución:**
```bash
# Asegúrate de tener el entorno virtual activado
venv\Scripts\activate

# Reinstala las dependencias
pip install -r requirements.txt
```

### Problema: "Address already in use"

**Solución:**
- Otro programa está usando el puerto 5000
- Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Cambiar a 5001
```

### Problema: Base de datos corrupta

**Solución:**
```bash
# Eliminar la base de datos
del database.db  # Windows
rm database.db   # Linux/Mac

# Reiniciar la aplicación (se creará automáticamente)
python app.py
```

### Problema: Errores de importación en VSCode

**Solución:**
1. Instala la extensión "Better Jinja"
2. Crea archivo `.vscode/settings.json`:
```json
{
    "files.associations": {
        "*.html": "jinja-html"
    }
}
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Desarrollado para la gestión eficiente de asignaciones de peritos**

- Sistema creado en 2025
- Versión: 1.0.0

---

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:

1. Revisa la sección de [Solución de Problemas](#solución-de-problemas)
2. Consulta la documentación
3. Abre un issue en el repositorio

---

## 🎉 Agradecimientos

- **TailwindCSS** por el framework de estilos
- **Font Awesome** por los iconos
- **Chart.js** por los gráficos interactivos
- **Flask** por el excelente framework web

---

## 📅 Historial de Versiones

### Versión 1.0.0 (2025-01-15)
- ✨ Lanzamiento inicial
- ✅ Gestión completa de asignaciones
- ✅ Sistema de calendario
- ✅ Búsqueda avanzada
- ✅ Reportes y estadísticas
- ✅ Exportación a Excel y PDF

---

## 🔮 Próximas Características

- [ ] Sistema de notificaciones por email
- [ ] Adjuntar documentos a asignaciones
- [ ] Módulo de usuarios y permisos
- [ ] Aplicación móvil
- [ ] Integración con calendario de Google
- [ ] Reportes personalizables
- [ ] Dashboard personalizable
- [ ] API REST completa

---

## 💡 Tips y Buenas Prácticas

### Backup de la Base de Datos
```bash
# Copiar manualmente
copy database.db database_backup.db  # Windows
cp database.db database_backup.db    # Linux/Mac

# O usar el sistema operativo para programar backups automáticos
```

### Rendimiento

- La base de datos SQLite soporta hasta 10,000+ registros sin problemas
- Para bases de datos más grandes, considera migrar a PostgreSQL
- Los reportes se generan en tiempo real

### Seguridad

- El sistema está diseñado para uso local
- Para producción, considera agregar:
  - Autenticación de usuarios
  - HTTPS
  - Validación adicional de datos
  - Rate limiting

---

**¡Gracias por usar SistemaPerito! 🎉**

Si este proyecto te fue útil, considera darle una ⭐ en GitHub.




📊 ESTRUCTURA DE BASE DE DATOS PROFESIONAL


1️⃣ TABLA: peritos
   - id
   - nombre_completo
   - tipo (Informático, Acústico, Antropólogo, Contable)
   - email (opcional)
   - telefono (opcional)
   - estado (Activo/Inactivo)
   - foto_perfil (opcional)

2️⃣ TABLA: asignaciones
   - id
   - numero_oficio
   - expediente
   - dependencia
   - tipo_perito
   - perito_id (relación con tabla peritos)
   - carpeta_fiscal
   - observaciones
   - lugar_completo
   - fecha_inicio
   - fecha_fin
   - perito_asignado
   - desginacion
   - oficio_desplazamiento
   - estado (Pendiente/En Proceso/Completado/Cancelado)
   - fecha_registro
   - hora_envio (dato de tu Excel)

3️⃣ TABLA: historial (para auditoría)
   - id
   - asignacion_id
   - accion (Creado/Modificado/Completado)
   - usuario
   - fecha_hora
   - detalles
```

---

## 🎯 FUNCIONALIDADES DINÁMICAS

### **Panel Principal con Cards Informativos:**
```
┌──────────────┬──────────────┬──────────────┐
│ 📊 Total     │ 🟢 Disponibles│ 🔴 Ocupados │
│ Asignaciones │   8 Peritos   │  3 Peritos  │
│     124      │               │             │
└──────────────┴──────────────┴──────────────┘

┌──────────────────────────────────────────┐
│ 📅 Asignaciones esta semana: 12          │
│ ⏰ Próximas a vencer: 3                  │
│ ✅ Completadas este mes: 45              │
└──────────────────────────────────────────┘
```

### **Formulario Inteligente de Registro:**
```
1. Seleccionas TIPO de perito
   ↓
2. Sistema muestra solo peritos de ese tipo
   ↓
3. Seleccionas FECHAS
   ↓
4. Sistema valida disponibilidad en TIEMPO REAL
   ↓
5. Si hay conflicto → Muestra alternativas
   ↓
6. Autocompletado de campos repetitivos
```

### **Validaciones Automáticas:**
```
✓ No permite fechas pasadas
✓ Fecha fin debe ser >= fecha inicio
✓ Alerta si el mismo oficio ya existe
✓ Detecta si el perito ya está asignado
✓ Calcula automáticamente días de asignación
✓ Formato correcto de oficios
```

---

## 📱 DISEÑO RESPONSIVE
```
💻 En computadora:
   - Vista de tabla completa
   - Múltiples columnas
   - Filtros laterales

📱 Si accedes desde celular (futuro):
   - Cards individuales
   - Menú hamburguesa
   - Vista simplificada
```

---

## 📤 EXPORTACIÓN AVANZADA
```
📊 Exportar a Excel:
   - Con filtros aplicados
   - Formato profesional
   - Colores y estilos
   - Gráficos automáticos

📄 Exportar a PDF:
   - Reporte por perito
   - Reporte por fechas
   - Estadísticas visuales
   - Logo personalizable
```

---

## 🔐 EXTRAS PROFESIONALES

### **1. Sistema de Estados:**
```
Asignación:
├── 📝 Pendiente (recién creada)
├── 🚗 En viaje (perito desplazándose)
├── 🔍 En proceso (realizando peritaje)
├── ✅ Completada (trabajo finalizado)
└── ❌ Cancelada (por algún motivo)
```

### **2. Notas y Observaciones:**
```
- Campo de texto libre para cada asignación
- Historial de modificaciones
- Adjuntar archivos (opcional - fase 2)
```

### **3. Reportes Automáticos:**
```
📈 Reporte mensual:
   - Peritos más asignados
   - Lugares más frecuentes
   - Tipos de peritaje más comunes
   - Tiempo promedio por asignación
```

---

## 🎨 PALETA DE COLORES SUGERIDA
```
Profesional y Moderna:

#1E40AF - Azul Principal (botones, headers)
#10B981 - Verde (disponible, éxito)
#EF4444 - Rojo (ocupado, alertas)
#F59E0B - Amarillo (advertencias)
#6B7280 - Gris (textos secundarios)
#F3F4F6 - Fondo claro
#FFFFFF - Blanco (cards)
```

---

## 📋 ESTRUCTURA DE CARPETAS
```
sistema-peritos/
├── app.py                 (Servidor Flask)
├── database.db            (Base de datos SQLite)
├── requirements.txt       (Dependencias Python)
├── README.md             (Instrucciones de uso)
├── templates/
│   ├── index.html        (Dashboard)
│   ├── nuevo.html        (Registrar asignación)
│   ├── buscar.html       (Búsqueda avanzada)
│   ├── calendario.html   (Vista calendario)
│   ├── peritos.html      (Gestión de peritos)
│   └── reportes.html     (Estadísticas)
├── static/
│   ├── css/
│   │   └── style.css     (Estilos personalizados)
│   ├── js/
│   │   └── app.js        (Funciones JavaScript)
│   └── images/
│       └── logo.png
└── exports/              (Carpeta para archivos exportados)