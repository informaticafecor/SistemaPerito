/**
 * SistemaPerito - Scripts Globales
 * Archivo: app.js
 * 
 * Funciones JavaScript reutilizables en todo el sistema
 */

// ============================================
// UTILIDADES GENERALES
// ============================================

/**
 * Formatear fecha en español
 * @param {string} fecha - Fecha en formato YYYY-MM-DD
 * @returns {string} Fecha formateada
 */
function formatearFecha(fecha) {
    const opciones = { year: 'numeric', month: 'long', day: 'numeric' };
    const fechaObj = new Date(fecha + 'T00:00:00');
    return fechaObj.toLocaleDateString('es-ES', opciones);
}

/**
 * Calcular días entre dos fechas
 * @param {string} fechaInicio - Fecha inicio
 * @param {string} fechaFin - Fecha fin
 * @returns {number} Número de días
 */
function calcularDias(fechaInicio, fechaFin) {
    const inicio = new Date(fechaInicio);
    const fin = new Date(fechaFin);
    const diferencia = fin - inicio;
    return Math.ceil(diferencia / (1000 * 60 * 60 * 24)) + 1;
}

/**
 * Mostrar notificación toast
 * @param {string} mensaje - Mensaje a mostrar
 * @param {string} tipo - Tipo: success, error, warning, info
 */
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg animate-fade-in ${getColorNotificacion(tipo)}`;
    notificacion.innerHTML = `
        <div class="flex items-center space-x-3">
            <i class="fas ${getIconoNotificacion(tipo)} text-xl"></i>
            <span class="font-semibold">${mensaje}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 hover:opacity-70">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notificacion);
    
    // Auto-eliminar después de 5 segundos
    setTimeout(() => {
        notificacion.classList.add('opacity-0');
        setTimeout(() => notificacion.remove(), 300);
    }, 5000);
}

/**
 * Obtener color de notificación según tipo
 */
function getColorNotificacion(tipo) {
    const colores = {
        success: 'bg-green-100 text-green-800 border-l-4 border-green-500',
        error: 'bg-red-100 text-red-800 border-l-4 border-red-500',
        warning: 'bg-yellow-100 text-yellow-800 border-l-4 border-yellow-500',
        info: 'bg-blue-100 text-blue-800 border-l-4 border-blue-500'
    };
    return colores[tipo] || colores.info;
}

/**
 * Obtener icono de notificación según tipo
 */
function getIconoNotificacion(tipo) {
    const iconos = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return iconos[tipo] || iconos.info;
}

// ============================================
// VALIDACIONES
// ============================================

/**
 * Validar formato de fecha
 * @param {string} fecha - Fecha a validar
 * @returns {boolean}
 */
function validarFecha(fecha) {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    if (!regex.test(fecha)) return false;
    
    const fechaObj = new Date(fecha);
    return fechaObj instanceof Date && !isNaN(fechaObj);
}

/**
 * Validar que fecha fin sea mayor o igual a fecha inicio
 * @param {string} fechaInicio
 * @param {string} fechaFin
 * @returns {boolean}
 */
function validarRangoFechas(fechaInicio, fechaFin) {
    return new Date(fechaFin) >= new Date(fechaInicio);
}

// ============================================
// ALMACENAMIENTO LOCAL
// ============================================

/**
 * Guardar preferencias del usuario
 * @param {string} clave
 * @param {any} valor
 */
function guardarPreferencia(clave, valor) {
    try {
        localStorage.setItem(`sistemaPerito_${clave}`, JSON.stringify(valor));
    } catch (error) {
        console.error('Error al guardar preferencia:', error);
    }
}

/**
 * Obtener preferencia del usuario
 * @param {string} clave
 * @param {any} valorPorDefecto
 * @returns {any}
 */
function obtenerPreferencia(clave, valorPorDefecto = null) {
    try {
        const valor = localStorage.getItem(`sistemaPerito_${clave}`);
        return valor ? JSON.parse(valor) : valorPorDefecto;
    } catch (error) {
        console.error('Error al obtener preferencia:', error);
        return valorPorDefecto;
    }
}

// ============================================
// UTILIDADES DE UI
// ============================================

/**
 * Mostrar/ocultar elemento con animación
 * @param {string} elementId - ID del elemento
 * @param {boolean} mostrar - true para mostrar, false para ocultar
 */
function toggleElemento(elementId, mostrar) {
    const elemento = document.getElementById(elementId);
    if (!elemento) return;
    
    if (mostrar) {
        elemento.classList.remove('hidden');
        elemento.classList.add('animate-fade-in');
    } else {
        elemento.classList.add('hidden');
        elemento.classList.remove('animate-fade-in');
    }
}

/**
 * Scroll suave a un elemento
 * @param {string} elementId - ID del elemento
 */
function scrollToElement(elementId) {
    const elemento = document.getElementById(elementId);
    if (elemento) {
        elemento.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// ============================================
// FORMATEO DE DATOS
// ============================================

/**
 * Capitalizar primera letra
 * @param {string} texto
 * @returns {string}
 */
function capitalize(texto) {
    if (!texto) return '';
    return texto.charAt(0).toUpperCase() + texto.slice(1).toLowerCase();
}

/**
 * Truncar texto
 * @param {string} texto
 * @param {number} longitud
 * @returns {string}
 */
function truncarTexto(texto, longitud = 50) {
    if (!texto) return '';
    if (texto.length <= longitud) return texto;
    return texto.substring(0, longitud) + '...';
}

// ============================================
// MANEJO DE ERRORES
// ============================================

/**
 * Manejar error de fetch
 * @param {Error} error
 */
function manejarErrorFetch(error) {
    console.error('Error en petición:', error);
    mostrarNotificacion('Error al conectar con el servidor', 'error');
}

// ============================================
// INICIALIZACIÓN
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ SistemaPerito - Scripts cargados correctamente');
    
    // Agregar año actual al footer
    const añoActual = new Date().getFullYear();
    const footers = document.querySelectorAll('footer');
    footers.forEach(footer => {
        if (footer.textContent.includes('2025')) {
            footer.textContent = footer.textContent.replace('2025', añoActual);
        }
    });
    
    // Agregar tooltips automáticos
    const elementosConTitulo = document.querySelectorAll('[title]');
    elementosConTitulo.forEach(elemento => {
        elemento.classList.add('tooltip');
        elemento.setAttribute('data-tooltip', elemento.getAttribute('title'));
        elemento.removeAttribute('title');
    });
});

// ============================================
// EXPORTAR FUNCIONES PARA USO GLOBAL
// ============================================

window.SistemaPerito = {
    formatearFecha,
    calcularDias,
    mostrarNotificacion,
    validarFecha,
    validarRangoFechas,
    guardarPreferencia,
    obtenerPreferencia,
    toggleElemento,
    scrollToElement,
    capitalize,
    truncarTexto
};