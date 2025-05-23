/**
 * Sistema de Historial para Calculadoras de Métodos Numéricos
 * 
 * Este módulo implementa funcionalidad para guardar, visualizar y
 * recuperar cálculos anteriores para diversas calculadoras.
 */

// Clase principal para gestionar el historial
class HistorialCalculadora {
    /**
     * Constructor del gestor de historial
     * @param {string} metodoId - Identificador único del método numérico (ej: 'bisection', 'cholesky')
     * @param {HTMLElement} containerElement - Elemento del DOM donde se mostrará el historial
     */
    constructor(metodoId, containerElement) {
        this.metodoId = metodoId;
        this.storageKey = `historial_${metodoId}`;
        this.containerElement = containerElement;
        this.historialItems = this.cargarHistorial();
        this.maxItems = 10; // Máximo número de elementos en el historial
    }

    /**
     * Carga el historial desde localStorage
     * @returns {Array} - Array de elementos del historial
     */
    cargarHistorial() {
        const historialJson = localStorage.getItem(this.storageKey);
        return historialJson ? JSON.parse(historialJson) : [];
    }

    /**
     * Guarda el historial en localStorage
     */
    guardarHistorial() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.historialItems));
    }

    /**
     * Añade un nuevo cálculo al historial
     * @param {Object} datos - Datos del cálculo a guardar
     */
    agregarCalculo(datos) {
        // Añadir timestamp al cálculo
        const nuevoCalculo = {
            ...datos,
            id: Date.now(),
            timestamp: new Date().toLocaleString()
        };

        // Añadir al inicio para que los más recientes aparezcan primero
        this.historialItems.unshift(nuevoCalculo);
        
        // Limitar el número de elementos
        if (this.historialItems.length > this.maxItems) {
            this.historialItems.pop();
        }
        
        this.guardarHistorial();
        this.renderizarHistorial();
    }

    /**
     * Elimina un cálculo del historial
     * @param {number} id - ID del cálculo a eliminar
     */
    eliminarCalculo(id) {
        this.historialItems = this.historialItems.filter(item => item.id !== id);
        this.guardarHistorial();
        this.renderizarHistorial();
    }

    /**
     * Limpia todo el historial
     */
    limpiarHistorial() {
        this.historialItems = [];
        this.guardarHistorial();
        this.renderizarHistorial();
    }

    /**
     * Renderiza el historial en el contenedor especificado
     */
    renderizarHistorial() {
        if (!this.containerElement) return;
        
        // Limpiar contenedor
        this.containerElement.innerHTML = '';
        
        // Si no hay elementos, mostrar mensaje
        if (this.historialItems.length === 0) {
            const emptyMsg = document.createElement('div');
            emptyMsg.className = 'text-center text-muted p-3';
            emptyMsg.textContent = 'No hay cálculos en el historial';
            this.containerElement.appendChild(emptyMsg);
            return;
        }
        
        // Crear lista para los elementos del historial
        const historialList = document.createElement('div');
        historialList.className = 'list-group';
        
        // Añadir cada elemento al historial
        this.historialItems.forEach(item => {
            const itemElement = this.crearElementoHistorial(item);
            historialList.appendChild(itemElement);
        });
        
        // Añadir botón para limpiar todo el historial
        const clearAllBtn = document.createElement('button');
        clearAllBtn.className = 'btn btn-sm btn-outline-danger mt-3';
        clearAllBtn.innerHTML = '<i class="bi bi-trash"></i> Limpiar historial';
        clearAllBtn.addEventListener('click', () => this.limpiarHistorial());
        
        // Añadir elementos al contenedor
        this.containerElement.appendChild(historialList);
        this.containerElement.appendChild(clearAllBtn);
    }

    /**
     * Crea un elemento HTML para un ítem del historial
     * @param {Object} item - Datos del cálculo
     * @returns {HTMLElement} - Elemento del DOM para el ítem
     */
    crearElementoHistorial(item) {
        const itemElement = document.createElement('div');
        itemElement.className = 'list-group-item list-group-item-action flex-column align-items-start';
        itemElement.dataset.id = item.id;
        
        // Cabecera con timestamp y acciones
        const header = document.createElement('div');
        header.className = 'd-flex w-100 justify-content-between';
        
        const timestamp = document.createElement('h6');
        timestamp.className = 'mb-1';
        timestamp.textContent = item.timestamp;
        
        const actions = document.createElement('div');
        actions.className = 'btn-group btn-group-sm';
        
        const loadBtn = document.createElement('button');
        loadBtn.className = 'btn btn-outline-primary';
        loadBtn.innerHTML = '<i class="bi bi-arrow-counterclockwise"></i>';
        loadBtn.title = 'Cargar este cálculo';
        loadBtn.addEventListener('click', () => this.cargarCalculo(item));
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-outline-danger';
        deleteBtn.innerHTML = '<i class="bi bi-trash"></i>';
        deleteBtn.title = 'Eliminar del historial';
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.eliminarCalculo(item.id);
        });
        
        actions.appendChild(loadBtn);
        actions.appendChild(deleteBtn);
        
        header.appendChild(timestamp);
        header.appendChild(actions);
        
        // Resumen del cálculo
        const content = document.createElement('div');
        content.className = 'mt-2';
        content.innerHTML = this.generarResumenCalculo(item);
        
        // Añadir todos los elementos
        itemElement.appendChild(header);
        itemElement.appendChild(content);
        
        // Hacer que el ítem sea clickeable para cargar el cálculo
        itemElement.addEventListener('click', () => this.cargarCalculo(item));
        
        return itemElement;
    }

    /**
     * Genera el HTML con el resumen del cálculo
     * @param {Object} item - Datos del cálculo
     * @returns {string} - HTML con el resumen
     */
    generarResumenCalculo(item) {
        // Este método puede ser sobrescrito por calculadoras específicas
        // Implementación básica que muestra parámetros y resultado
        let html = '<div class="small">';
        
        // Parámetros (si existen)
        if (item.parametros) {
            html += '<strong>Parámetros:</strong> ';
            html += Object.entries(item.parametros)
                .map(([key, value]) => `${key}: ${value}`)
                .join(', ');
        }
        
        // Puntos (para métodos con coordenadas)
        if (item.puntos && item.puntos.length) {
            html += '<br><strong>Puntos:</strong> ';
            html += item.puntos.slice(0, 3)
                .map(p => `(${p.x}, ${p.fx})`)
                .join(', ');
            
            if (item.puntos.length > 3) {
                html += ` y ${item.puntos.length - 3} más`;
            }
        }
        
        // Matriz (si existe)
        if (item.matriz) {
            html += '<br><strong>Matriz:</strong> ';
            html += `${item.matriz.length}×${item.matriz[0].length}`;
        }
        
        // Resultado (si existe)
        if (item.resultado !== undefined) {
            let resultadoStr = typeof item.resultado === 'object' 
                ? JSON.stringify(item.resultado).slice(0, 50) 
                : item.resultado;
                
            html += `<br><strong>Resultado:</strong> ${resultadoStr}`;
            
            // Si el resultado es muy largo, truncarlo
            if (resultadoStr.length > 50) {
                html += '...';
            }
        }
        
        html += '</div>';
        return html;
    }

    /**
     * Carga un cálculo previo en la calculadora
     * @param {Object} item - Datos del cálculo a cargar
     */
    cargarCalculo(item) {
        // Este método debe ser implementado por cada calculadora específica
        // Se dispara un evento personalizado que la calculadora puede escuchar
        const event = new CustomEvent('historial:cargar', { 
            detail: { item }
        });
        document.dispatchEvent(event);
        
        console.log(`Cargando cálculo del ${item.timestamp}`);
    }
}

/**
 * Adaptador de Historial para el Método de Bisección
 */
class HistorialBiseccion extends HistorialCalculadora {
    constructor(containerElement) {
        super('bisection', containerElement);
    }
    
    // Sobrescribir método para personalizar el resumen
    generarResumenCalculo(item) {
        let html = '<div class="small">';
        html += `<strong>Ecuación:</strong> ${item.parametros.equation}<br>`;
        html += `<strong>Intervalo:</strong> [${item.parametros.a}, ${item.parametros.b}]<br>`;
        html += `<strong>Raíz encontrada:</strong> ${item.resultado?.toFixed(6) || 'N/A'}`;
        html += '</div>';
        return html;
    }
    
    // Sobrescribir método para implementar la carga específica
    cargarCalculo(item) {
        if (!item.parametros) return;
        
        // Rellenar los campos del formulario
        document.getElementById('equation').value = item.parametros.equation;
        document.getElementById('intervalA').value = item.parametros.a;
        document.getElementById('intervalB').value = item.parametros.b;
        document.getElementById('tolerance').value = item.parametros.tol;
        document.getElementById('maxIterations').value = item.parametros.maxIterations;
        
        // Disparar evento personalizado
        super.cargarCalculo(item);
    }
}

/**
 * Adaptador de Historial para Factorización de Cholesky
 */
class HistorialCholesky extends HistorialCalculadora {
    constructor(containerElement) {
        super('cholesky', containerElement);
    }
    
    generarResumenCalculo(item) {
        let html = '<div class="small">';
        html += `<strong>Matriz:</strong> ${item.matriz.length}×${item.matriz[0].length}<br>`;
        
        // Mostrar una vista previa de la matriz (primeras 2 filas, primeras 3 columnas)
        html += '<div class="matrix-preview mt-1 mb-2">';
        for (let i = 0; i < Math.min(2, item.matriz.length); i++) {
            html += '<div class="matrix-row">';
            for (let j = 0; j < Math.min(3, item.matriz[i].length); j++) {
                html += `<span class="matrix-cell">${item.matriz[i][j]}</span>`;
            }
            if (item.matriz[i].length > 3) {
                html += '<span class="matrix-cell">...</span>';
            }
            html += '</div>';
        }
        if (item.matriz.length > 2) {
            html += '<div class="matrix-row"><span class="matrix-cell">...</span></div>';
        }
        html += '</div>';
        
        // Mostrar el estado de la solución
        if (item.resultado) {
            if (Array.isArray(item.resultado)) {
                html += '<strong>Solución:</strong> [';
                html += item.resultado.slice(0, 3).map(x => x.toFixed(4)).join(', ');
                if (item.resultado.length > 3) {
                    html += ', ...';
                }
                html += ']';
            } else {
                html += `<strong>Estado:</strong> ${item.resultado}`;
            }
        }
        
        html += '</div>';
        return html;
    }
    
    cargarCalculo(item) {
        if (!item.matriz) return;
        
        // Actualizar dimensiones de la matriz
        document.getElementById('inputM').value = item.matriz.length;
        document.getElementById('inputN').value = item.matriz[0].length;
        
        // Generar la matriz
        generateMatrix(); // Asumiendo que esta función está disponible globalmente
        
        // Rellenar los valores de la matriz
        setTimeout(() => {
            for (let i = 0; i < item.matriz.length; i++) {
                for (let j = 0; j < item.matriz[i].length; j++) {
                    const input = document.querySelector(`.matrix-input[data-row="${i}"][data-col="${j}"]`);
                    if (input) {
                        input.value = item.matriz[i][j];
                    }
                }
            }
        }, 100); // Pequeño retraso para asegurar que la matriz se haya generado
        
        super.cargarCalculo(item);
    }
}

/**
 * Adaptador de Historial para Trazadores Cúbicos (Cubic Spline)
 */
class HistorialCubicSpline extends HistorialCalculadora {
    constructor(containerElement) {
        super('cubic-spline', containerElement);
    }
    
    generarResumenCalculo(item) {
        let html = '<div class="small">';
        
        // Resumen de puntos
        if (item.puntos && item.puntos.length) {
            html += `<strong>Puntos:</strong> ${item.puntos.length} puntos<br>`;
            html += '<div class="points-preview mt-1 mb-2">';
            for (let i = 0; i < Math.min(3, item.puntos.length); i++) {
                const p = item.puntos[i];
                html += `(${p.x}, ${p.fx})`;
                if (i < Math.min(3, item.puntos.length) - 1) html += ', ';
            }
            if (item.puntos.length > 3) {
                html += ', ...';
            }
            html += '</div>';
        }
        
        // Parámetros
        if (item.parametros) {
            html += `<strong>Tipo:</strong> ${item.parametros.boundary || 'Natural'}<br>`;
            html += `<strong>Valor interpolado:</strong> x = ${item.parametros.x_interp}`;
        }
        
        // Resultado
        if (item.resultado !== undefined) {
            html += `<br><strong>Resultado:</strong> ${item.resultado.toFixed(6)}`;
        }
        
        html += '</div>';
        return html;
    }
    
    cargarCalculo(item) {
        if (!item.puntos || !item.parametros) return;
        
        // Limpiar puntos existentes
        if (typeof points !== 'undefined') {
            points.length = 0;
        }
        
        // Añadir los puntos
        item.puntos.forEach(punto => {
            if (typeof points !== 'undefined') {
                points.push({
                    x: punto.x,
                    fx: punto.fx,
                    selected: true
                });
            }
        });
        
        // Actualizar la tabla de puntos
        if (typeof renderPoints === 'function') {
            renderPoints();
        }
        
        // Establecer parámetros
        if (item.parametros) {
            document.getElementById('valueToInterpolate').value = item.parametros.x_interp;
            
            const boundarySelect = document.getElementById('boundary');
            if (boundarySelect) {
                boundarySelect.value = item.parametros.boundary || 'natural';
                
                // Disparar el evento change para mostrar/ocultar campos relevantes
                const event = new Event('change');
                boundarySelect.dispatchEvent(event);
            }
            
            // Establecer valores para condiciones específicas
            if (item.parametros.boundary === 'clamped' && item.parametros.deriv_start !== undefined) {
                document.getElementById('derivStart').value = item.parametros.deriv_start;
                document.getElementById('derivEnd').value = item.parametros.deriv_end;
            }
            
            if (item.parametros.boundary === 'periodic' && item.parametros.periodic_check !== undefined) {
                document.getElementById('periodicCheck').checked = item.parametros.periodic_check;
            }
        }
        
        super.cargarCalculo(item);
    }
}

/**
 * Adaptador de Historial para Método de Diferencias Divididas
 */
class HistorialDiferenciasDivididas extends HistorialCalculadora {
    constructor(containerElement) {
        super('divided-differences', containerElement);
    }
    
    generarResumenCalculo(item) {
        let html = '<div class="small">';
        
        // Información básica
        if (item.parametros) {
            html += `<strong>Grado:</strong> ${item.parametros.degree}<br>`;
            html += `<strong>Valor a interpolar:</strong> x = ${item.parametros.x_interp}<br>`;
        }
        
        // Resumen de puntos
        if (item.puntos && item.puntos.length) {
            html += `<strong>Puntos:</strong> ${item.puntos.length} puntos<br>`;
            html += '<div class="points-preview mt-1 mb-2">';
            for (let i = 0; i < Math.min(3, item.puntos.length); i++) {
                const p = item.puntos[i];
                html += `(${p.x}, ${p.fx})`;
                if (i < Math.min(3, item.puntos.length) - 1) html += ', ';
            }
            if (item.puntos.length > 3) {
                html += ', ...';
            }
            html += '</div>';
        }
        
        // Resultado
        if (item.resultado !== undefined) {
            html += `<strong>Resultado:</strong> ${item.resultado.toFixed(6)}`;
        }
        
        html += '</div>';
        return html;
    }
    
    cargarCalculo(item) {
        if (!item.puntos || !item.parametros) return;
        
        // Limpiar puntos existentes
        if (typeof points !== 'undefined') {
            points.length = 0;
        }
        
        // Añadir los puntos
        item.puntos.forEach(punto => {
            if (typeof points !== 'undefined') {
                points.push({
                    x: punto.x,
                    fx: punto.fx,
                    selected: punto.selected !== undefined ? punto.selected : true
                });
            }
        });
        
        // Actualizar la tabla de puntos
        if (typeof updatePointsTable === 'function') {
            updatePointsTable();
        }
        
        // Establecer parámetros
        if (item.parametros) {
            document.getElementById('degree').value = item.parametros.degree;
            document.getElementById('valueToInterpolate').value = item.parametros.x_interp;
            
            // Actualizar la validación
            if (typeof updateValidation === 'function') {
                updateValidation();
            }
        }
        
        super.cargarCalculo(item);
    }
}

/**
 * Adaptador de Historial para Eliminación Gaussiana
 */
class HistorialGaussiana extends HistorialCalculadora {
    constructor(containerElement, metodoPivoteo = false) {
        const metodoId = metodoPivoteo ? 'gauss-pivoting' : 'gauss-back';
        super(metodoId, containerElement);
        this.conPivoteo = metodoPivoteo;
    }
    
    generarResumenCalculo(item) {
        let html = '<div class="small">';
        
        // Información sobre la matriz
        if (item.matriz) {
            html += `<strong>Matriz:</strong> ${item.matriz.length}×${item.matriz[0].length}<br>`;
            
            // Vista previa de la matriz
            html += '<div class="matrix-preview mt-1 mb-2">';
            for (let i = 0; i < Math.min(2, item.matriz.length); i++) {
                html += '<div class="matrix-row">';
                for (let j = 0; j < Math.min(3, item.matriz[i].length); j++) {
                    html += `<span class="matrix-cell">${item.matriz[i][j]}</span>`;
                }
                if (item.matriz[i].length > 3) {
                    html += '<span class="matrix-cell">...</span>';
                }
                html += '</div>';
            }
            if (item.matriz.length > 2) {
                html += '<div class="matrix-row"><span class="matrix-cell">...</span></div>';
            }
            html += '</div>';
        }
        
        // Resultado
        if (item.resultado) {
            if (Array.isArray(item.resultado)) {
                html += '<strong>Solución:</strong> [';
                html += item.resultado.slice(0, 3).map(x => x.toFixed(4)).join(', ');
                if (item.resultado.length > 3) {
                    html += ', ...';
                }
                html += ']';
            } else if (typeof item.resultado === 'string') {
                // Si el resultado es un mensaje (e.g., sistema inconsistente)
                html += `<strong>Estado:</strong> ${item.resultado.substring(0, 50)}`;
                if (item.resultado.length > 50) {
                    html += '...';
                }
            }
        }
        
        html += '</div>';
        return html;
    }
    
    cargarCalculo(item) {
        if (!item.matriz) return;
        
        // Actualizar dimensiones de la matriz
        document.getElementById('inputM').value = item.matriz.length;
        document.getElementById('inputN').value = item.matriz[0].length;
        
        // Generar la matriz
        if (typeof generateMatrix === 'function') {
            generateMatrix();
        }
        
        // Pequeño retraso para asegurar que la matriz se haya generado
        setTimeout(() => {
            // Rellenar los valores de la matriz
            for (let i = 0; i < item.matriz.length; i++) {
                for (let j = 0; j < item.matriz[i].length; j++) {
                    const input = document.querySelector(`.matrix-input[data-row="${i}"][data-col="${j}"]`);
                    if (input) {
                        input.value = item.matriz[i][j];
                    }
                }
            }
        }, 100);
        
        super.cargarCalculo(item);
    }
}

/**
 * Función para inicializar el historial en una calculadora
 * @param {string} metodoId - Identificador del método numérico
 * @param {Object} adaptadores - Mapa de adaptadores disponibles
 * @returns {HistorialCalculadora} - Instancia del gestor de historial
 */
function inicializarHistorial(metodoId) {
    // Crear el contenedor del historial si no existe
    let historialContainer = document.getElementById('historialContainer');
    
    if (!historialContainer) {
        // Crear el panel del historial
        const historialPanel = document.createElement('div');
        historialPanel.className = 'historial-panel card mt-4';
        historialPanel.innerHTML = `
            <div class="card-header d-flex justify-content-between align-items-center bg-light">
                <h5 class="mb-0">
                    <button class="btn btn-link" type="button" data-bs-toggle="collapse" 
                            data-bs-target="#historialCollapse" aria-expanded="false">
                        <i class="bi bi-clock-history"></i> Historial de cálculos
                    </button>
                </h5>
                <span class="badge bg-primary rounded-pill" id="historialCount">0</span>
            </div>
            <div class="collapse" id="historialCollapse">
                <div class="card-body p-0" id="historialContainer">
                    <!-- Aquí se mostrarán los cálculos anteriores -->
                </div>
            </div>
        `;
        
        // Insertar el panel antes del contenedor de respuesta
        const responseContainer = document.getElementById('responseContainer');
        if (responseContainer) {
            responseContainer.parentNode.insertBefore(historialPanel, responseContainer);
        } else {
            // Si no hay contenedor de respuesta, añadirlo al final de la calculadora
            const calculatorSection = document.getElementById('calculator');
            if (calculatorSection) {
                calculatorSection.appendChild(historialPanel);
            }
        }
        
        historialContainer = document.getElementById('historialContainer');
    }
    
    // Crear el adaptador de historial según el método
    let historialManager;
    
    switch (metodoId) {
        case 'bisection':
            historialManager = new HistorialBiseccion(historialContainer);
            break;
        case 'cholesky':
            historialManager = new HistorialCholesky(historialContainer);
            break;
        case 'cubic-spline':
            historialManager = new HistorialCubicSpline(historialContainer);
            break;
        case 'divided-differences':
            historialManager = new HistorialDiferenciasDivididas(historialContainer);
            break;
        case 'gauss-back':
            historialManager = new HistorialGaussiana(historialContainer, false);
            break;
        case 'gauss-pivoting':
            historialManager = new HistorialGaussiana(historialContainer, true);
            break;
        default:
            historialManager = new HistorialCalculadora(metodoId, historialContainer);
    }
    
    // Actualizar contador de elementos del historial
    const historialCount = document.getElementById('historialCount');
    if (historialCount) {
        historialCount.textContent = historialManager.historialItems.length;
    }
    
    // Renderizar el historial inicial
    historialManager.renderizarHistorial();
    
    return historialManager;
}

// Estilos CSS para el historial
function agregarEstilosHistorial() {
    const style = document.createElement('style');
    style.textContent = `
        .historial-panel {
            margin-bottom: 20px;
        }
        
        .historial-panel .card-header {
            padding: 0.5rem 1rem;
        }
        
        .historial-panel .btn-link {
            color: #0d6efd;
            text-decoration: none;
            padding: 0;
        }
        
        .historial-panel .list-group-item {
            padding: 10px 15px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .historial-panel .list-group-item:hover {
            background-color: #f8f9fa;
        }
        
        .matrix-preview, .points-preview {
            font-family: monospace;
            font-size: 0.8rem;
        }
        
        .matrix-row {
            white-space: nowrap;
        }
        
        .matrix-cell {
            display: inline-block;
            min-width: 30px;
            text-align: right;
            margin-right: 5px;
        }
        
        /* Estilos para versión responsive */
        @media (max-width: 768px) {
            .historial-panel .card-header h5 {
                font-size: 1rem;
            }
        }
    `;
    document.head.appendChild(style);
}

// Función para integrar el historial en una calculadora
function integrarHistorialEnCalculadora(metodoId, capturarParametrosCallback) {
    // Agregar estilos CSS necesarios
    agregarEstilosHistorial();
    
    // Inicializar el gestor de historial
    const historialManager = inicializarHistorial(metodoId);
    
    // Integrar con la calculadora: interceptar el botón de cálculo
    // (Esta implementación debe adaptarse a cada calculadora)
    const calculate = window.calculate; // Preservar la función original
    
    window.calculate = function() {
        // Ejecutar el cálculo original
        calculate.apply(this, arguments);
        
        // Obtener parámetros y resultados usando el callback
        setTimeout(() => {
            if (typeof capturarParametrosCallback === 'function') {
                const datosCalculo = capturarParametrosCallback();
                if (datosCalculo) {
                    historialManager.agregarCalculo(datosCalculo);
                    
                    // Actualizar contador
                    const historialCount = document.getElementById('historialCount');
                    if (historialCount) {
                        historialCount.textContent = historialManager.historialItems.length;
                    }
                }
            }
        }, 500); // Pequeño retraso para que se complete el cálculo
    };
    
    return historialManager;
}

// Exportar las funciones y clases necesarias
window.HistorialCalculadora = HistorialCalculadora;
window.inicializarHistorial = inicializarHistorial;
window.integrarHistorialEnCalculadora = integrarHistorialEnCalculadora;