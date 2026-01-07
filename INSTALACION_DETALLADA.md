# 🔧 GUÍA DE INSTALACIÓN DETALLADA - SistemaPerito

Esta guía cubre la instalación paso a paso con capturas y solución de problemas.

--- ANTES DE ENVIAR UN GIT PULL HHACER ESTO

 git reset --hard HEAD
 git pull
--------------------------


## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación de Python](#instalación-de-python)
3. [Descarga del Proyecto](#descarga-del-proyecto)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Instalación de Dependencias](#instalación-de-dependencias)
6. [Primera Ejecución](#primera-ejecución)
7. [Verificación de Instalación](#verificación-de-instalación)
8. [Problemas Comunes](#problemas-comunes)

---

## 💻 Requisitos del Sistema

### Requisitos Mínimos:
- **Sistema Operativo**: Windows 7+, macOS 10.12+, o Linux (Ubuntu 18.04+)
- **RAM**: 2 GB mínimo (4 GB recomendado)
- **Espacio en Disco**: 500 MB libres
- **Procesador**: Cualquier CPU moderna
- **Conexión a Internet**: Solo para instalación inicial

### Software Necesario:
- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

---

## 🐍 Instalación de Python

### Windows:

1. **Descargar Python**:
   - Ve a: https://www.python.org/downloads/
   - Descarga la última versión (ejemplo: Python 3.12.1)

2. **Ejecutar el Instalador**:
```
   ⚠️ IMPORTANTE: Marca la casilla "Add Python to PATH"
```
   - Ejecuta el archivo descargado
   - ✅ Marca: **"Add Python to PATH"**
   - Clic en **"Install Now"**
   - Espera a que termine la instalación

3. **Verificar Instalación**:
```bash
   # Abre CMD y ejecuta:
   python --version
   
   # Deberías ver algo como:
   # Python 3.12.1
```

### macOS:

1. **Opción A - Desde python.org**:
   - Descarga el instalador de https://www.python.org/downloads/
   - Ejecuta el instalador .pkg
   - Sigue las instrucciones

2. **Opción B - Con Homebrew** (recomendado):
```bash
   # Instala Homebrew si no lo tienes:
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Instala Python:
   brew install python
```

3. **Verificar**:
```bash
   python3 --version
```

### Linux (Ubuntu/Debian):
```bash
# Actualizar repositorios
sudo apt update

# Instalar Python 3 y pip
sudo apt install python3 python3-pip python3-venv

# Verificar
python3 --version
pip3 --version
```

---

## 📥 Descarga del Proyecto

### Opción 1: Descarga Directa

1. Descarga todos los archivos del proyecto
2. Crea una carpeta llamada `SistemaPerito`
3. Coloca todos los archivos dentro

Estructura final:
```
SistemaPerito/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── nuevo.html
│   ├── buscar.html
│   ├── calendario.html
│   ├── peritos.html
│   └── reportes.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

### Opción 2: Con Git
```bash
# Clona el repositorio
git clone https://github.com/tuusuario/SistemaPerito.git

# Entra a la carpeta
cd SistemaPerito
```

---

## ⚙️ Configuración del Entorno

### Paso 1: Abrir Terminal en la Carpeta del Proyecto

**Windows**:
- Abre la carpeta `SistemaPerito`
- Mantén presionado `Shift` y haz clic derecho
- Selecciona "Abrir ventana de PowerShell aquí" o "Abrir en Terminal"

**macOS/Linux**:
- Abre Terminal
- Navega a la carpeta:
```bash
  cd /ruta/a/SistemaPerito
```

### Paso 2: Crear Entorno Virtual

**Windows**:
```bash
python -m venv venv
```

**macOS/Linux**:
```bash
python3 -m venv venv
```

**Qué hace esto**:
- Crea una carpeta `venv` con un entorno aislado de Python
- Evita conflictos con otras instalaciones de Python
- Mantiene el proyecto organizado

**Tiempo estimado**: 30-60 segundos

### Paso 3: Activar Entorno Virtual

**Windows (CMD)**:
```bash
venv\Scripts\activate
```

**Windows (PowerShell)**:
```bash
venv\Scripts\Activate.ps1
```

Si aparece error en PowerShell:
```bash
# Ejecuta esto primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego activa:
venv\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
source venv/bin/activate
```

**Verificación**:
Verás `(venv)` al inicio de tu línea de comandos:
```
(venv) C:\Users\TuUsuario\SistemaPerito>
```

✅ **Esto confirma que el entorno virtual está activo**

---

## 📦 Instalación de Dependencias

### Método 1: Usando requirements.txt (Recomendado)
```bash
pip install -r requirements.txt
```

**Salida esperada**:
```
Collecting Flask==3.0.0
  Downloading Flask-3.0.0-py3-none-any.whl
Collecting openpyxl==3.1.2
  Downloading openpyxl-3.1.2-py2.py3-none-any.whl
Collecting reportlab==4.0.7
  Downloading reportlab-4.0.7-py3-none-any.whl
...
Successfully installed Flask-3.0.0 openpyxl-3.1.2 reportlab-4.0.7 ...
```

**Tiempo estimado**: 1-3 minutos (dependiendo de tu conexión)

### Método 2: Instalación Manual

Si `requirements.txt` no funciona:
```bash
pip install flask
pip install openpyxl
pip install reportlab
```

### Verificar Instalación de Dependencias
```bash
pip list
```

Deberías ver al menos:
```
Flask                3.0.0
openpyxl            3.1.2
reportlab           4.0.7
Werkzeug            3.0.1
```

---

## 🚀 Primera Ejecución

### Paso 1: Ejecutar el Servidor
```bash
python app.py
```

**Salida esperada**:
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
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Paso 2: Abrir en el Navegador

1. Abre tu navegador (Chrome, Firefox, Edge, Safari)
2. Ve a: `http://127.0.0.1:5000`
3. Deberías ver el **Dashboard** del sistema

### Paso 3: Verificar Base de Datos

Automáticamente se creará:
- `database.db` (archivo SQLite)
- Con 11 peritos precargados
- Tablas: peritos, asignaciones, historial

---

## ✅ Verificación de Instalación

### Checklist de Verificación:
```
☐ Python instalado correctamente (python --version funciona)
☐ Entorno virtual creado (carpeta venv existe)
☐ Entorno virtual activado ((venv) aparece en terminal)
☐ Dependencias instaladas (pip list muestra Flask, etc.)
☐ Servidor ejecutándose (sin errores en terminal)
☐ Dashboard visible en navegador
☐ Base de datos creada (archivo database.db existe)
☐ 11 peritos visibles en menú "Peritos"
```

### Prueba Funcional:

1. **Dashboard**: Verifica que se vea correctamente
2. **Nueva Asignación**: Crea una asignación de prueba
3. **Peritos**: Verifica que aparezcan los 11 peritos
4. **Calendario**: Verifica que cargue el calendario
5. **Búsqueda**: Busca la asignación creada
6. **Reportes**: Verifica que se muestren gráficos

---

## 🐛 Problemas Comunes

### Problema 1: "python no se reconoce como comando"

**Causa**: Python no está en el PATH del sistema

**Soluciones**:

**Opción A - Reinstalar Python**:
1. Desinstala Python
2. Reinstala marcando "Add Python to PATH"

**Opción B - Agregar manualmente al PATH**:
1. Busca dónde está instalado Python (ej: `C:\Python312`)
2. Agrégalo al PATH:
   - Windows: Buscar "Variables de entorno" → Editar PATH → Agregar ruta

**Opción C - Usar py en lugar de python**:
```bash
py -m venv venv
py app.py
```

### Problema 2: Error al activar entorno virtual en PowerShell

**Error**:
```
cannot be loaded because running scripts is disabled on this system
```

**Solución**:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema 3: "ModuleNotFoundError: No module named 'flask'"

**Causa**: Flask no está instalado o el entorno virtual no está activado

**Solución**:
```bash
# 1. Verifica que el entorno virtual esté activado
#    Debe aparecer (venv) en la terminal

# 2. Si no está activado:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Reinstala Flask:
pip install flask openpyxl reportlab
```

### Problema 4: "Address already in use" - Puerto 5000 ocupado

**Causa**: Otro programa está usando el puerto 5000

**Solución A - Cambiar puerto**:
Edita `app.py` línea final:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Cambia a 5001
```

**Solución B - Cerrar programa que usa el puerto**:

**Windows**:
```bash
# Ver qué programa usa el puerto 5000
netstat -ano | findstr :5000

# Cerrar el proceso (reemplaza PID con el número que aparece)
taskkill /PID <PID> /F
```

**Linux/Mac**:
```bash
# Ver qué programa usa el puerto 5000
lsof -i :5000

# Cerrar el proceso
kill -9 <PID>
```

### Problema 5: La página no carga estilos (se ve sin formato)

**Causa**: No hay conexión a internet (TailwindCSS se carga desde CDN)

**Soluciones**:
1. Verifica tu conexión a internet
2. Refresca la página (Ctrl + F5)
3. Cambia de navegador

### Problema 6: Error "PermissionError" al crear venv

**Causa**: Falta de permisos o antivirus bloqueando

**Soluciones**:
1. Ejecuta el terminal como administrador
2. Desactiva temporalmente el antivirus
3. Crea el venv en una carpeta donde tengas permisos

### Problema 7: Base de datos corrupta

**Síntomas**:
- Errores al guardar datos
- No aparecen los peritos
- Errores en consola sobre SQLite

**Solución**:
```bash
# 1. Detén el servidor (Ctrl + C)

# 2. Elimina la base de datos
del database.db  # Windows
rm database.db   # Linux/Mac

# 3. Reinicia el servidor
python app.py
# Se creará una nueva base de datos limpia
```

### Problema 8: Lentitud en el sistema

**Causas posibles**:
- Muchos registros en la base de datos (>10,000)
- Computadora con pocos recursos

**Soluciones**:
1. Exporta y limpia registros antiguos
2. Cierra otros programas
3. Considera migrar a PostgreSQL para mejor rendimiento

---

## 📞 Soporte Adicional

Si ninguna de estas soluciones funciona:

1. Verifica los requisitos del sistema
2. Asegúrate de tener Python 3.8+
3. Intenta en otra computadora
4. Consulta la documentación de Flask: https://flask.palletsprojects.com/

---

## ✨ Próximos Pasos

Una vez instalado correctamente:

1. ✅ Lee la `GUIA_RAPIDA.md`
2. ✅ Crea tus primeras asignaciones de prueba
3. ✅ Explora todas las funcionalidades
4. ✅ Configura backups automáticos
5. ✅ Personaliza según tus necesidades

---

**¡Felicidades! Has instalado SistemaPerito exitosamente. 🎉**