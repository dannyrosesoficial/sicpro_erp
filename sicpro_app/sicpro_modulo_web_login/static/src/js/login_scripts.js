/**
 * SICPRO ERP - Lógica de Interfaz de Usuario
 * Ubicación: America/Havana
 */

document.addEventListener('DOMContentLoaded', function() {

    // 1. Configuración de Partículas
    if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
        particlesJS("particles-js", {
            "particles": {
                "number": { "value": 40 },
                "color": { "value": "#ffffff" },
                "opacity": { "value": 0.1 },
                "size": { "value": 2 },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#ffffff",
                    "opacity": 0.05
                },
                "move": { "enable": true, "speed": 0.5 }
            }
        });
    }

    // 2. Reloj Cuba (Actualización cada segundo)
    function updateClock() {
        const now = new Date();
        const options = {
            timeZone: 'America/Havana',
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        const clockEl = document.getElementById('live-clock');
        if (clockEl) {
            clockEl.innerText = now.toLocaleTimeString('es-CU', options);
        }
    }

    setInterval(updateClock, 1000);
    updateClock();
});

// 3. Toggle Password (Fuera del DOMContentLoaded para que sea accesible globalmente)
window.togglePassword = function() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');

    if (passwordInput && toggleIcon) {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }
};