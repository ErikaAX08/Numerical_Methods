/**
 * Archivo de integración del sistema de historial con cada calculadora
 * Incluye ejemplos de implementación para cada método numérico
 */

// Integración con la calculadora de Método de Bisección
function integrarHistorialBiseccion() {
    return integrarHistorialEnCalculadora('bisection', function() {
        // Capturar los parámetros del cálculo
        const equation = document.getElementById('equation').value;
        const a = parseFloat(document.getElementById('intervalA').value);
        const b = parseFloat(document.getElementById('intervalB').value);
        const tol = parseFloat(document.getElementById('tolerance').value);
        const maxIterations = parseInt(document.getElementById('maxIterations').value);
        
        // Obtener el resultado si está disponible
        let resultado;
        const resultMsg = document.querySelector('.alert-success strong');
        if (resultMsg && resultMsg.textContent.includes('Root found')) {
            const resultText = resultMsg.nextSibling.textContent.trim();
            resultado = parseFloat(resultText);
        }
        
        return {
            parametros: {
                equation,
                a,
                b,
                tol,
                maxIterations
            },
            resultado
        };
    });
}

// Integración con la calculadora de Factorización de Cholesky
function integrarHistorialCholesky() {
    return integrarHistorialEnCalculadora('cholesky', function() {
        // Capturar la matriz ingresada
        const rows = parseInt(document.getElementById('inputM').value);
        const cols = parseInt(document.getElementById('inputN').value);
        
        const matriz = [];
        for (let i = 0; i < rows; i++) {
            const rowValues = [];
            for (let j = 0; j < cols; j++) {
                const input = document.querySelector(`.matrix-input[data-row="${i}"][data-col="${j}"]`);
                if (input) {
                    rowValues.push(parseFloat(input.value));
                }
            }
            matriz.push(rowValues);
        }
        
        // Obtener el resultado si está disponible
        let resultado;
        const resultContainer = document.getElementById('resultContainer');
        if (resultContainer) {
            const successAlert = resultContainer.querySelector('.alert-success');
            if (successAlert) {
                // Intentar obtener la solución del sistema
                const solutionItems = successAlert.querySelectorAll('li');
                if (solutionItems.length > 0) {
                    resultado = Array.from(solutionItems).map(item => {
                        const valueText = item.textContent.split('=')[1].trim();
                        return parseFloat(valueText);
                    });
                }
            } else {
                // Si no hay éxito, podría ser un mensaje de error o estado
                const warningAlert = resultContainer.querySelector('.alert-warning, .alert-danger, .alert-info');
                if (warningAlert) {
                    const messageP = warningAlert.querySelector('p');
                    if (messageP) {
                        resultado = messageP.textContent;
                    }
                }
            }
        }
        
        return { matriz, resultado };
    });
}

// Integración con la calculadora de Cubic Spline
function integrarHistorialCubicSpline() {
    return integrarHistorialEnCalculadora('cubic-spline', function() {
        // Obtener los puntos seleccionados
        const puntos = window.points ? window.points.filter(p => p.selected).map(p => ({
            x: parseFloat(p.x),
            fx: parseFloat(p.fx)
        })) : [];
        
        // Obtener los parámetros
        const x_interp = parseFloat(document.getElementById('valueToInterpolate').value);
        const boundary = document.getElementById('boundary').value;
        
        const parametros = { x_interp, boundary };
        
        // Parámetros adicionales según el tipo de condición de frontera
        if (boundary === 'clamped') {
            parametros.deriv_start = parseFloat(document.getElementById('derivStart').value);
            parametros.deriv_end = parseFloat(document.getElementById('derivEnd').value);
        } else if (boundary === 'periodic') {
            parametros.periodic_check = document.getElementById('periodicCheck').checked;
        }
        
        // Obtener el resultado si está disponible
        let resultado;
        const resultContainer = document.getElementById('resultContainer');
        if (resultContainer) {
            const successAlert = resultContainer.querySelector('.alert-success');
            if (successAlert) {
                const resultText = successAlert.querySelector('h4').textContent;
                const resultValue = resultText.split(':')[1].trim();
                resultado = parseFloat(resultValue);
            }
        }
        
        return { puntos, parametros, resultado };
    });
}

// Integración con la calculadora de Diferencias Divididas
function integrarHistorialDiferenciasDivididas() {
    return integrarHistorialEnCalculadora('divided-differences', function() {
        // Obtener los puntos seleccionados
        const puntos = window.points ? window.points.filter(p => p.selected).map(p => ({
            x: parseFloat(p.x),
            fx: parseFloat(p.fx),
            selected: true
        })) : [];
        
        // Obtener parámetros
        const degree = parseInt(document.getElementById('degree').value);
        const x_interp = parseFloat(document.getElementById('valueToInterpolate').value);
        
        // Obtener el resultado si está disponible
        let resultado;
        const resultContainer = document.getElementById('resultContainer');
        if (resultContainer) {
            const successAlert = resultContainer.querySelector('.alert-success');
            if (successAlert) {
                const resultText = successAlert.querySelector('h4').textContent;
                const resultValue = resultText.split('=')[1].trim();
                resultado = parseFloat(resultValue);
            }
        }
        
        return {
            puntos,
            parametros: { degree, x_interp },
            resultado
        };
    });
}

// Integración con la calculadora de Eliminación Gaussiana (sin pivoteo)
function integrarHistorialGaussBack() {
    return integrarHistorialEnCalculadora('gauss-back', function() {
        // Capturar la matriz ingresada
        const rows = parseInt(document.getElementById('inputM').value);
        const cols = parseInt(document.getElementById('inputN').value);
        
        const matriz = [];
        for (let i = 0; i < rows; i++) {
            const rowValues = [];
            for (let j = 0; j < cols; j++) {
                const input = document.querySelector(`.matrix-input[data-row="${i}"][data-col="${j}"]`);
                if (input) {
                    rowValues.push(parseFloat(input.value));
                }
            }
            matriz.push(rowValues);
        }
        
        // Obtener el resultado
        let resultado;
        const resultContainer = document.getElementById('resultContainer');
        if (resultContainer) {
            const successAlert = resultContainer.querySelector('.alert-success');
            if (successAlert) {
                // Intentar obtener la solución del sistema
                const solutionItems = successAlert.querySelectorAll('li');
                if (solutionItems.length > 0) {
                    resultado = Array.from(solutionItems).map(item => {
                        const valueText = item.textContent.split('=')[1].trim();
                        return parseFloat(valueText);
                    });
                }
            } else {
                // Si no hay éxito, podría ser un mensaje de error o estado
                const altAlert = resultContainer.querySelector('.alert-warning, .alert-danger, .alert-info');
                if (altAlert) {
                    const messageP = altAlert.querySelector('p');
                    if (messageP) {
                        resultado = messageP.textContent;
                    }
                }
            }
        }
        
        return { matriz, resultado };
    });
}

// Integración con la calculadora de Eliminación Gaussiana con pivoteo
function integrarHistorialGaussPivoting() {
    return integrarHistorialEnCalculadora('gauss-pivoting', function() {
        // Capturar la matriz ingresada
        const rows = parseInt(document.getElementById('inputM').value);
        const cols = parseInt(document.getElementById('inputN').value);
        
        const matriz = [];
        for (let i = 0; i < rows; i++) {
            const rowValues = [];
            for (let j = 0; j < cols; j++) {
                const input = document.querySelector(`.matrix-input[data-row="${i}"][data-col="${j}"]`);
                if (input) {
                    rowValues.push(parseFloat(input.value));
                }
            }
            matriz.push(rowValues);
        }
        
        // Obtener el resultado
        let resultado;
        const resultContainer = document.getElementById('resultContainer');
        if (resultContainer) {
            const successAlert = resultContainer.querySelector('.alert-success');
            if (successAlert) {
                // Intentar obtener la solución del sistema
                const valueTexts = successAlert.querySelectorAll('p');
                if (valueTexts.length > 0) {
                    resultado = Array.from(valueTexts).map(p => {
                        const valueText = p.textContent.split('=')[1];
                        if (valueText) {
                            return parseFloat(valueText.trim());
                        }
                        return null;
                    }).filter(v => v !== null);
                }
            } else {
                // Si no hay éxito, podría ser un mensaje de error o estado
                const altAlert = resultContainer.querySelector('.alert-warning, .alert-danger, .alert-info');
                if (altAlert) {
                    const messageP = altAlert.querySelector('p');
                    if (messageP) {
                        resultado = messageP.textContent;
                    }
                }
            }
        }
        
        return { matriz, resultado };
    });
}

// Función principal para detectar e integrar el historial con la calculadora actual
document.addEventListener('DOMContentLoaded', function() {
    // Detectar qué calculadora está activa basándonos en elementos de la página
    setTimeout(function() {
        let historialManager;
        
        if (document.getElementById('equation') && document.getElementById('intervalA')) {
            console.log("Detectada calculadora: Método de Bisección");
            historialManager = integrarHistorialBiseccion();
        } 
        else if (document.getElementById('boundary') && document.getElementById('calculatorForm')) {
            console.log("Detectada calculadora: Cubic Spline");
            historialManager = integrarHistorialCubicSpline();
        }
        else if (document.getElementById('degree') && document.getElementById('valueToInterpolate')) {
            console.log("Detectada calculadora: Diferencias Divididas");
            historialManager = integrarHistorialDiferenciasDivididas();
        }
        else if (document.getElementById('matrixTable') && document.getElementById('clearBtn')) {
            // Diferenciar entre las variantes de eliminación gaussiana
            // Esta detección es aproximada, podría necesitar refinamiento
            const title = document.querySelector('h2.display-4');
            if (title && title.textContent.includes('Maximum Column Pivoting')) {
                console.log("Detectada calculadora: Eliminación Gaussiana con Pivoteo");
                historialManager = integrarHistorialGaussPivoting();
            } 
            else if (title && title.textContent.includes('back replacement')) {
                console.log("Detectada calculadora: Eliminación Gaussiana con Sustitución");
                historialManager = integrarHistorialGaussBack();
            }
            else {
                console.log("Detectada calculadora: Factorización de Cholesky");
                historialManager = integrarHistorialCholesky();
            }
        }
        
        if (historialManager) {
            console.log("Sistema de historial integrado correctamente");
        }
    }, 1000); // Dar tiempo para que la página se cargue completamente
});