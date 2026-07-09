/** @odoo-module **/

document.addEventListener('DOMContentLoaded', function() {

    // === 1. GESTIÓN DE TEMA (DARK/LIGHT) - EJECUCIÓN PRIORITARIA ===
    const themeBtn = document.getElementById('themeBtn');
    const body = document.body;

    // Recuperar el tema guardado o usar 'dark' por defecto para evitar fogonazos blancos
    const savedTheme = localStorage.getItem('sicpro_theme') || 'light';
    body.setAttribute('data-bs-theme', savedTheme);

    // Configuración inicial del icono del botón según el tema cargado
    if (themeBtn) {
        themeBtn.innerHTML = savedTheme === 'dark'
            ? '<i class="fa fa-sun-o" style="color: #FFD700;"></i>'
            : '<i class="fa fa-moon-o" style="color: #714B67;"></i>';

        // Evento Click para cambiar el tema
        themeBtn.addEventListener('click', () => {
            const currentTheme = body.getAttribute('data-bs-theme');

            if (currentTheme === 'light') {
                body.setAttribute('data-bs-theme', 'dark');
                // Al estar en oscuro, el botón muestra el sol para volver a la luz
                themeBtn.innerHTML = '<i class="fa fa-sun-o" style="color: #FFD700;"></i>';
                localStorage.setItem('sicpro_theme', 'dark');
            } else {
                body.setAttribute('data-bs-theme', 'light');
                // Al estar en claro, el botón muestra la luna para volver a la oscuridad
                themeBtn.innerHTML = '<i class="fa fa-moon-o" style="color: #714B67;"></i>';
                localStorage.setItem('sicpro_theme', 'light');
            }
        });
    }

    // === 2. INICIALIZACIÓN DE AOS (ANIMACIONES) ===
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true
        });
    }

    // === 3. BUSCADOR DINÁMICO ===
    const searchInput = document.getElementById('dirSearch');

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const filter = this.value.toLowerCase().trim();
            const items = document.querySelectorAll('.dir-item');

            items.forEach(item => {
                const text = item.innerText.toLowerCase();

                if (text.includes(filter)) {
                    // Mostrar elemento con transiciones suaves
                    item.style.display = "";
                    // Usamos un pequeño timeout para que la transición de opacidad funcione
                    setTimeout(() => {
                        item.style.opacity = "1";
                        item.style.transform = "scale(1)";
                    }, 10);
                } else {
                    // Ocultar elemento
                    item.style.opacity = "0";
                    item.style.transform = "scale(0.95)";
                    // Esperar a que termine la animación para poner display none
                    setTimeout(() => {
                        if (item.style.opacity === "0") {
                            item.style.display = "none";
                        }
                    }, 300);
                }
            });

            // Refrescar AOS para que las animaciones se recalculen al filtrar
            if (typeof AOS !== 'undefined') {
                AOS.refresh();
            }
        });
    }
});