"""
SistemaPerito - Sistema de Gestión de Asignaciones de Peritos
Autor: Desarrollado para control de asignaciones
Fecha: 2025
Descripción: Sistema web para gestionar asignaciones de peritos con validación
de disponibilidad, búsqueda avanzada y exportación de reportes.
"""

from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import json
from datetime import datetime, timedelta
import os

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Inicializar aplicación Flask
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Para caracteres especiales en español

# ============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================================================

def init_db():
    """
    Inicializa la base de datos SQLite creando las tablas necesarias
    si no existen. Se ejecuta al iniciar la aplicación.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabla de peritos con información básica
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS peritos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            estado TEXT DEFAULT 'Activo',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de asignaciones con toda la información del Excel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asignaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hoja_envio TEXT,
            expediente TEXT,
            dependencia TEXT,
            tipo_perito TEXT,
            carpeta_fiscal TEXT,
            observaciones TEXT,
            lugar TEXT,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            perito_asignado TEXT NOT NULL,
            perito_id INTEGER,
            desginacion TEXT,
            oficio_desplazamiento TEXT,
            estado TEXT DEFAULT 'Pendiente',
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (perito_id) REFERENCES peritos (id)
        )
    ''')
    
    # Tabla de historial para auditoría
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asignacion_id INTEGER,
            accion TEXT NOT NULL,
            detalles TEXT,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (asignacion_id) REFERENCES asignaciones (id)
        )
    ''')
    
    conn.commit()
    
    # Insertar peritos iniciales si la tabla está vacía
    cursor.execute('SELECT COUNT(*) FROM peritos')
    if cursor.fetchone()[0] == 0:
        peritos_iniciales = [
            # Peritos Informáticos
            ('ALBERTO HONORATO BLACIDO QUITO', 'Informático'),
            ('MISAEL EDSON PALOMINO AYLAS', 'Informático'),
            ('LUIS ALBERTO VILLANUEVA HUAMAN', 'Informático'),
            # Peritos Acústicos
            ('MARCIAL SULCA CAHUANA', 'Acústico'),
            ('EDILBERTO EDISON ZAVALA CAMPOS', 'Acústico'),
            ('WILBER PAUL ESPINOZA LAUREANO', 'Acústico'),
            # Peritos Antropólogos
            ('BRIAN BARRY SOTO ALCAZAR', 'Antropólogo'),
            ('SANDRA LISBET IBARRA APAZA', 'Antropólogo'),
            # Peritos Contables
            ('ROSARIO CORDERO BORJA', 'Contable'),
            ('ANGELA ROXANA CALDERON BUSTAMANTE', 'Contable'),
            ('YESENIA ELIZABETH CHAVEZ VALERO', 'Contable')
        ]
        
        cursor.executemany(
            'INSERT INTO peritos (nombre_completo, tipo) VALUES (?, ?)',
            peritos_iniciales
        )
        conn.commit()
    
    conn.close()


def actualizar_estados_automaticos():
    """
    Actualiza automáticamente los estados de las asignaciones según las fechas
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    hoy = datetime.now().date()
    
    # Cambiar a "En Proceso" si la fecha de inicio es hoy o pasó
    cursor.execute('''
        UPDATE asignaciones 
        SET estado = "En Proceso"
        WHERE estado = "Pendiente" 
        AND date(fecha_inicio) <= date('now')
        AND date(fecha_fin) >= date('now')
    ''')
    
    # Cambiar a "Completado" si la fecha de fin ya pasó
    cursor.execute('''
        UPDATE asignaciones 
        SET estado = "Completado"
        WHERE estado IN ("Pendiente", "En Proceso")
        AND date(fecha_fin) < date('now')
    ''')
    
    conn.commit()
    conn.close()


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================


def verificar_disponibilidad(perito_id, fecha_inicio, fecha_fin, asignacion_id=None):
    """
    Verifica si un perito está disponible en un rango de fechas.
    
    Args:
        perito_id: ID del perito a verificar
        fecha_inicio: Fecha de inicio de la asignación (formato: YYYY-MM-DD)
        fecha_fin: Fecha de fin de la asignación (formato: YYYY-MM-DD)
        asignacion_id: ID de asignación a excluir (para ediciones)
    
    Returns:
        tuple: (disponible: bool, conflictos: list)
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Convertir fechas a formato comparable
    fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d')
    
    # Buscar asignaciones que se solapen en fechas
    query = '''
        SELECT id, expediente, fecha_inicio, fecha_fin, observaciones
        FROM asignaciones
        WHERE perito_id = ?
        AND estado != 'Cancelado'
        AND (
            (fecha_inicio <= ? AND fecha_fin >= ?) OR
            (fecha_inicio <= ? AND fecha_fin >= ?) OR
            (fecha_inicio >= ? AND fecha_fin <= ?)
        )
    '''
    
    params = [
        perito_id,
        fecha_fin, fecha_inicio,
        fecha_fin, fecha_fin,
        fecha_inicio, fecha_fin
    ]
    
    # Excluir la asignación actual si estamos editando
    if asignacion_id:
        query += ' AND id != ?'
        params.append(asignacion_id)
    
    cursor.execute(query, params)
    conflictos = cursor.fetchall()
    conn.close()
    
    disponible = len(conflictos) == 0
    
    return disponible, conflictos

def registrar_historial(asignacion_id, accion, detalles=''):
    """
    Registra una acción en el historial para auditoría.
    
    Args:
        asignacion_id: ID de la asignación relacionada
        accion: Tipo de acción (Creado, Modificado, Completado, etc.)
        detalles: Información adicional sobre la acción
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO historial (asignacion_id, accion, detalles) VALUES (?, ?, ?)',
        (asignacion_id, accion, detalles)
    )
    
    conn.commit()
    conn.close()

# ============================================================================
# RUTAS PRINCIPALES
# ============================================================================

@app.route('/')
def index():
    """
    Página principal - Dashboard con estadísticas generales
    """
    # Actualizar estados automáticamente
    actualizar_estados_automaticos()
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Obtener estadísticas generales
    cursor.execute('SELECT COUNT(*) FROM asignaciones')
    total_asignaciones = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM asignaciones WHERE estado = "Pendiente"')
    pendientes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM asignaciones WHERE estado = "En Proceso"')
    en_proceso = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM asignaciones WHERE estado = "Completado"')
    completados = cursor.fetchone()[0]
    
    # Obtener asignaciones recientes (últimas 10)
    cursor.execute('''
        SELECT a.id, a.hoja_envio, a.expediente, a.dependencia, 
               a.tipo_perito, a.carpeta_fiscal, a.observaciones, a.lugar,
               a.fecha_inicio, a.fecha_fin, a.perito_asignado, a.perito_id,
               a.desginacion, a.oficio_desplazamiento, a.estado, a.fecha_registro,
               p.nombre_completo
        FROM asignaciones a
        LEFT JOIN peritos p ON a.perito_id = p.id
        WHERE a.estado != "Cancelado"
        ORDER BY a.fecha_registro DESC
        LIMIT 10
    ''')
    
    asignaciones_recientes = []
    for row in cursor.fetchall():
        asignaciones_recientes.append({
            'id': row[0],
            'hoja_envio': row[1],
            'expediente': row[2],
            'dependencia': row[3],
            'tipo_perito': row[4],
            'fecha_inicio': row[8],
            'fecha_fin': row[9],
            'perito': row[16] or row[10],  # nombre_completo o perito_asignado
            'estado': row[14],
            'lugar': row[7]
        })
    
    conn.close()
    
    return render_template('index.html',
                         total=total_asignaciones,
                         pendientes=pendientes,
                         en_proceso=en_proceso,
                         completados=completados,
                         asignaciones=asignaciones_recientes)

@app.route('/nuevo')
def nuevo():
    """
    Página para registrar nueva asignación
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Obtener lista de peritos activos
    cursor.execute('SELECT id, nombre_completo, tipo FROM peritos WHERE estado = "Activo" ORDER BY tipo, nombre_completo')
    peritos = cursor.fetchall()
    conn.close()
    
    # Organizar peritos por tipo
    peritos_por_tipo = {
        'Informático': [],
        'Acústico': [],
        'Antropólogo': [],
        'Contable': []
    }
    
    for perito in peritos:
        peritos_por_tipo[perito[2]].append({
            'id': perito[0],
            'nombre': perito[1]
        })
    
    return render_template('nuevo.html', peritos=peritos_por_tipo)

@app.route('/buscar')
def buscar():
    """
    Página de búsqueda avanzada
    """
    return render_template('buscar.html')

@app.route('/calendario')
def calendario():
    """
    Vista de calendario con asignaciones
    """
    return render_template('calendario.html')

@app.route('/peritos')
def peritos():
    """
    Gestión de peritos
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM peritos ORDER BY tipo, nombre_completo')
    peritos_list = []
    
    for row in cursor.fetchall():
        # Contar asignaciones del perito
        cursor.execute('SELECT COUNT(*) FROM asignaciones WHERE perito_id = ?', (row[0],))
        total_asignaciones = cursor.fetchone()[0]
        
        peritos_list.append({
            'id': row[0],
            'nombre': row[1],
            'tipo': row[2],
            'estado': row[3],
            'total_asignaciones': total_asignaciones
        })
    
    conn.close()
    
    return render_template('peritos.html', peritos=peritos_list)

@app.route('/reportes')
def reportes():
    """
    Página de reportes y estadísticas
    """
    return render_template('reportes.html')

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/asignaciones', methods=['GET'])
def get_asignaciones():
    """
    Obtiene todas las asignaciones con filtros opcionales
    Query params: estado, perito_id, fecha_desde, fecha_hasta
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Construir query con filtros
    query = '''
        SELECT a.*, p.nombre_completo
        FROM asignaciones a
        LEFT JOIN peritos p ON a.perito_id = p.id
        WHERE 1=1
    '''
    params = []
    
    # Filtro por estado
    if request.args.get('estado'):
        query += ' AND a.estado = ?'
        params.append(request.args.get('estado'))
    
    # Filtro por perito
    if request.args.get('perito_id'):
        query += ' AND a.perito_id = ?'
        params.append(request.args.get('perito_id'))
    
    # Filtro por rango de fechas
    if request.args.get('fecha_desde'):
        query += ' AND a.fecha_inicio >= ?'
        params.append(request.args.get('fecha_desde'))
    
    if request.args.get('fecha_hasta'):
        query += ' AND a.fecha_fin <= ?'
        params.append(request.args.get('fecha_hasta'))
    
    query += ' ORDER BY a.fecha_inicio DESC'
    
    cursor.execute(query, params)
    
    asignaciones = []
    for row in cursor.fetchall():
        asignaciones.append({
            'id': row[0],
            'hoja_envio': row[1],
            'expediente': row[2],
            'dependencia': row[3],
            'tipo_perito': row[4],
            'carpeta_fiscal': row[5],
            'observaciones': row[6],
            'lugar': row[7],
            'fecha_inicio': row[8],
            'fecha_fin': row[9],
            'perito_asignado': row[10],
            'desginacion': row[12],
            'oficio_desplazamiento': row[13],
            'estado': row[14],
            'perito_nombre': row[16]
        })
    
    conn.close()
    return jsonify(asignaciones)





@app.route('/api/asignacion/<int:id>', methods=['GET'])
def get_asignacion(id):
    """
    Obtiene una asignación específica por ID
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, p.nombre_completo
        FROM asignaciones a
        LEFT JOIN peritos p ON a.perito_id = p.id
        WHERE a.id = ?
    ''', (id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        asignacion = {
            'id': row[0],
            'hoja_envio': row[1],
            'expediente': row[2],
            'dependencia': row[3],
            'tipo_perito': row[4],
            'carpeta_fiscal': row[5],
            'observaciones': row[6],
            'lugar': row[7],
            'fecha_inicio': row[8],
            'fecha_fin': row[9],
            'perito_asignado': row[10],
            'perito_id': row[11],
            'desginacion': row[12],
            'oficio_desplazamiento': row[13],
            'estado': row[14],
            'perito_nombre': row[16]
        }
        return jsonify(asignacion)
    else:
        return jsonify({'error': 'Asignación no encontrada'}), 404

@app.route('/api/asignacion', methods=['POST'])
def crear_asignacion():
    """
    Crea una nueva asignación
    """
    data = request.json
    
    # Validar datos requeridos
    if not all(k in data for k in ('perito_id', 'fecha_inicio', 'fecha_fin')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Verificar disponibilidad del perito
    disponible, conflictos = verificar_disponibilidad(
        data['perito_id'],
        data['fecha_inicio'],
        data['fecha_fin']
    )
    
    if not disponible:
        return jsonify({
            'error': 'El perito no está disponible en estas fechas',
            'conflictos': conflictos
        }), 409
    
    # Insertar asignación
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO asignaciones (
            hoja_envio, expediente, dependencia, tipo_perito,
            carpeta_fiscal, observaciones, lugar, fecha_inicio,
            fecha_fin, perito_asignado, perito_id, desginacion,
            oficio_desplazamiento, estado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('hoja_envio', ''),
        data.get('expediente', ''),
        data.get('dependencia', ''),
        data.get('tipo_perito', ''),
        data.get('carpeta_fiscal', ''),
        data.get('observaciones', ''),
        data.get('lugar', ''),
        data['fecha_inicio'],
        data['fecha_fin'],
        data.get('perito_asignado', ''),
        data['perito_id'],
        data.get('desginacion', ''),
        data.get('oficio_desplazamiento', ''),
        'Pendiente'
    ))
    
    asignacion_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Registrar en historial
    registrar_historial(asignacion_id, 'Creado', 'Asignación creada exitosamente')
    
    return jsonify({
        'success': True,
        'id': asignacion_id,
        'message': 'Asignación creada exitosamente'
    }), 201

@app.route('/api/asignacion/<int:id>', methods=['PUT'])
def actualizar_asignacion(id):
    """
    Actualiza una asignación existente
    """
    data = request.json
    
    # Si se están cambiando las fechas, verificar disponibilidad
    if 'fecha_inicio' in data and 'fecha_fin' in data and 'perito_id' in data:
        disponible, conflictos = verificar_disponibilidad(
            data['perito_id'],
            data['fecha_inicio'],
            data['fecha_fin'],
            asignacion_id=id
        )
        
        if not disponible:
            return jsonify({
                'error': 'El perito no está disponible en estas fechas',
                'conflictos': conflictos
            }), 409
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Construir query de actualización dinámicamente
    campos = []
    valores = []
    
    campos_permitidos = [
        'hoja_envio', 'expediente', 'dependencia', 'tipo_perito',
        'carpeta_fiscal', 'observaciones', 'lugar', 'fecha_inicio',
        'fecha_fin', 'perito_asignado', 'perito_id', 'desginacion',
        'oficio_desplazamiento', 'estado'
    ]
    
    for campo in campos_permitidos:
        if campo in data:
            campos.append(f'{campo} = ?')
            valores.append(data[campo])
    
    if not campos:
        return jsonify({'error': 'No hay campos para actualizar'}), 400
    
    valores.append(id)
    query = f"UPDATE asignaciones SET {', '.join(campos)} WHERE id = ?"
    
    cursor.execute(query, valores)
    conn.commit()
    conn.close()
    
    # Registrar en historial
    registrar_historial(id, 'Modificado', f'Campos actualizados: {", ".join(campos)}')
    
    return jsonify({
        'success': True,
        'message': 'Asignación actualizada exitosamente'
    })

# ------------------------------------------------------

@app.route('/api/asignacion/<int:id>', methods=['DELETE'])
def eliminar_asignacion(id):
    """
    Elimina (marca como cancelada) una asignación
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Verificar que la asignación existe
    cursor.execute('SELECT * FROM asignaciones WHERE id = ?', (id,))
    asignacion = cursor.fetchone()
    
    if not asignacion:
        conn.close()
        return jsonify({'error': 'Asignación no encontrada'}), 404
    
    # Marcar como cancelada en lugar de eliminar
    cursor.execute('UPDATE asignaciones SET estado = "Cancelado" WHERE id = ?', (id,))
    
    conn.commit()
    conn.close()
    
    # Registrar en historial
    registrar_historial(id, 'Cancelado', 'Asignación cancelada por el usuario')
    
    return jsonify({
        'success': True,
        'message': 'Asignación cancelada exitosamente'
    })


@app.route('/api/asignacion/<int:id>/cambiar-estado', methods=['PUT'])
def cambiar_estado_asignacion(id):
    """
    Cambia el estado de una asignación
    """
    data = request.json
    nuevo_estado = data.get('estado')
    
    if nuevo_estado not in ['Pendiente', 'En Proceso', 'Completado', 'Cancelado']:
        return jsonify({'error': 'Estado inválido'}), 400
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE asignaciones SET estado = ? WHERE id = ?', (nuevo_estado, id))
    conn.commit()
    conn.close()
    
    # Registrar en historial
    registrar_historial(id, 'Modificado', f'Estado cambiado a: {nuevo_estado}')
    
    return jsonify({
        'success': True,
        'message': f'Estado actualizado a {nuevo_estado}'
    })



@app.route('/api/verificar-disponibilidad', methods=['POST'])
def api_verificar_disponibilidad():
    """
    Verifica disponibilidad de un perito en tiempo real
    """
    data = request.json
    
    if not all(k in data for k in ('perito_id', 'fecha_inicio', 'fecha_fin')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    disponible, conflictos = verificar_disponibilidad(
        data['perito_id'],
        data['fecha_inicio'],
        data['fecha_fin'],
        data.get('asignacion_id')
    )
    
    return jsonify({
        'disponible': disponible,
        'conflictos': [{
            'id': c[0],
            'expediente': c[1],
            'fecha_inicio': c[2],
            'fecha_fin': c[3],
            'observaciones': c[4]
        } for c in conflictos]
    })

@app.route('/api/peritos', methods=['GET'])
def get_peritos():
    """
    Obtiene lista de todos los peritos
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM peritos WHERE estado = "Activo" ORDER BY tipo, nombre_completo')
    
    peritos = []
    for row in cursor.fetchall():
        peritos.append({
            'id': row[0],
            'nombre': row[1],
            'tipo': row[2],
            'estado': row[3]
        })
    
    conn.close()
    return jsonify(peritos)

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    """
    Obtiene estadísticas generales del sistema
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Total de asignaciones por estado
    cursor.execute('''
        SELECT estado, COUNT(*) 
        FROM asignaciones 
        GROUP BY estado
    ''')
    por_estado = dict(cursor.fetchall())
    
    # Asignaciones por tipo de perito
    cursor.execute('''
        SELECT tipo_perito, COUNT(*) 
        FROM asignaciones 
        WHERE tipo_perito != ""
        GROUP BY tipo_perito
    ''')
    por_tipo = dict(cursor.fetchall())
    
    # Peritos más asignados
    cursor.execute('''
        SELECT p.nombre_completo, COUNT(a.id) as total
        FROM peritos p
        LEFT JOIN asignaciones a ON p.id = a.perito_id
        GROUP BY p.id
        ORDER BY total DESC
        LIMIT 5
    ''')
    top_peritos = [{'nombre': row[0], 'total': row[1]} for row in cursor.fetchall()]
    
    # Asignaciones por mes (últimos 6 meses)
    cursor.execute('''
        SELECT strftime('%Y-%m', fecha_inicio) as mes, COUNT(*) as total
        FROM asignaciones
        WHERE fecha_inicio >= date('now', '-6 months')
        GROUP BY mes
        ORDER BY mes
    ''')
    por_mes = [{'mes': row[0], 'total': row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'por_estado': por_estado,
        'por_tipo': por_tipo,
        'top_peritos': top_peritos,
        'por_mes': por_mes
    })

@app.route('/api/buscar', methods=['GET'])
def buscar_asignaciones():
    """
    Búsqueda avanzada de asignaciones
    Query params: q (término de búsqueda), campo (campo específico)
    """
    termino = request.args.get('q', '').strip()
    campo = request.args.get('campo', 'todos')
    
    if not termino:
        return jsonify([])
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Construir query según el campo
    if campo == 'todos':
        query = '''
            SELECT a.*, p.nombre_completo
            FROM asignaciones a
            LEFT JOIN peritos p ON a.perito_id = p.id
            WHERE a.hoja_envio LIKE ? 
            OR a.expediente LIKE ?
            OR a.carpeta_fiscal LIKE ?
            OR a.lugar LIKE ?
            OR p.nombre_completo LIKE ?
            ORDER BY a.fecha_inicio DESC
        '''
        params = [f'%{termino}%'] * 5
    else:
        query = f'''
            SELECT a.*, p.nombre_completo
            FROM asignaciones a
            LEFT JOIN peritos p ON a.perito_id = p.id
            WHERE a.{campo} LIKE ?
            ORDER BY a.fecha_inicio DESC
        '''
        params = [f'%{termino}%']
    
    cursor.execute(query, params)
    
    resultados = []
    for row in cursor.fetchall():
        resultados.append({
            'id': row[0],
            'hoja_envio': row[1],
            'expediente': row[2],
            'dependencia': row[3],
            'tipo_perito': row[4],
            'carpeta_fiscal': row[5],
            'observaciones': row[6],
            'lugar': row[7],
            'fecha_inicio': row[8],
            'fecha_fin': row[9],
            'perito_asignado': row[10],
            'desginacion': row[12],
            'estado': row[14],
            'perito_nombre': row[16]
        })
    
    conn.close()
    return jsonify(resultados)

# ============================================================================
# EXPORTACIÓN DE DATOS
# ============================================================================

@app.route('/api/exportar/excel', methods=['GET'])
def exportar_excel():
    """
    Exporta asignaciones a formato Excel con formato profesional
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Obtener filtros de la query string
    query = '''
        SELECT a.*, p.nombre_completo
        FROM asignaciones a
        LEFT JOIN peritos p ON a.perito_id = p.id
        WHERE 1=1
    '''
    params = []
    
    if request.args.get('estado'):
        query += ' AND a.estado = ?'
        params.append(request.args.get('estado'))
    
    if request.args.get('fecha_desde'):
        query += ' AND a.fecha_inicio >= ?'
        params.append(request.args.get('fecha_desde'))
    
    if request.args.get('fecha_hasta'):
        query += ' AND a.fecha_fin <= ?'
        params.append(request.args.get('fecha_hasta'))
    
    query += ' ORDER BY a.fecha_inicio DESC'
    
    cursor.execute(query, params)
    datos = cursor.fetchall()
    conn.close()
    
    # Crear libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Asignaciones"
    
    # Estilos
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="1E40AF", end_color="1E40AF", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Encabezados
    headers = [
        'ID', 'Hoja Envío', 'Expediente', 'Dependencia', 'Tipo Perito',
        'Carpeta Fiscal', 'Observaciones', 'Lugar', 'Fecha Inicio',
        'Fecha Fin', 'Perito Asignado', 'Designación', 'Oficio Desplazamiento',
        'Estado', 'Fecha Registro'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border
    
    # Datos
    for row_idx, row_data in enumerate(datos, 2):
        for col_idx, value in enumerate(row_data[:15], 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border
            cell.alignment = Alignment(wrap_text=True)
            
            # Color según estado
            if col_idx == 14:  # Columna de estado
                if value == 'Completado':
                    cell.fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
                elif value == 'En Proceso':
                    cell.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
                elif value == 'Pendiente':
                    cell.fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
                elif value == 'Cancelado':
                    cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    
    # Ajustar ancho de columnas
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column].width = adjusted_width
    
    # Guardar archivo
    filename = f'asignaciones_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    filepath = os.path.join('exports', filename)
    
    # Crear carpeta exports si no existe
    os.makedirs('exports', exist_ok=True)
    
    wb.save(filepath)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/api/exportar/pdf', methods=['GET'])
def exportar_pdf():
    """
    Exporta asignaciones a formato PDF con tabla profesional
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Obtener datos (similar al Excel)
    query = '''
        SELECT a.hoja_envio, a.expediente, a.fecha_inicio, a.fecha_fin, 
               p.nombre_completo, a.estado, a.lugar
        FROM asignaciones a
        LEFT JOIN peritos p ON a.perito_id = p.id
        WHERE 1=1
    '''
    params = []
    
    if request.args.get('estado'):
        query += ' AND a.estado = ?'
        params.append(request.args.get('estado'))
    
    query += ' ORDER BY a.fecha_inicio DESC LIMIT 50'
    
    cursor.execute(query, params)
    datos = cursor.fetchall()
    conn.close()
    
    # Crear PDF
    filename = f'reporte_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join('exports', filename)
    os.makedirs('exports', exist_ok=True)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Título
    title = Paragraph("<b>REPORTE DE ASIGNACIONES DE PERITOS</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Fecha del reporte
    fecha_reporte = Paragraph(
        f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        styles['Normal']
    )
    elements.append(fecha_reporte)
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de datos
    data = [['Oficio', 'Expediente', 'F. Inicio', 'F. Fin', 'Perito', 'Estado', 'Lugar']]
    
    for row in datos:
        data.append([
            row[0][:15] if row[0] else '',
            row[1][:15] if row[1] else '',
            row[2],
            row[3],
            row[4][:25] if row[4] else '',
            row[5],
            row[6][:20] if row[6] else ''
        ])
    
    table = Table(data, colWidths=[1.2*inch, 1.2*inch, 0.9*inch, 0.9*inch, 1.8*inch, 0.9*inch, 1.5*inch])
    
    # Estilo de la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(table)
    
    # Construir PDF
    doc.build(elements)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

# ============================================================================
# INICIALIZACIÓN Y EJECUCIÓN
# ============================================================================

if __name__ == '__main__':
    # Inicializar base de datos
    init_db()
    
    print("=" * 60)
    print("🚀 SISTEMA PERITO - Iniciado")
    print("=" * 60)
    print("📍 URL: http://127.0.0.1:5000")
    print("📊 Dashboard: http://127.0.0.1:5000")
    print("➕ Nueva Asignación: http://127.0.0.1:5000/nuevo")
    print("🔍 Búsqueda: http://127.0.0.1:5000/buscar")
    print("📅 Calendario: http://127.0.0.1:5000/calendario")
    print("👥 Peritos: http://127.0.0.1:5000/peritos")
    print("📈 Reportes: http://127.0.0.1:5000/reportes")
    print("=" * 60)
    print("💡 Presiona CTRL+C para detener el servidor")
    print("=" * 60)
    
    # Ejecutar aplicación en modo desarrollo
    app.run(debug=True, host='127.0.0.1', port=5000)