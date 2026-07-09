/**
 * SICPRO Admin Logic & Particles
 * Developer: Danny Rose's 🌹
 */

function initAdminLogic() {
    const bridgeElement = document.getElementById('os_key');
    const dom_key = bridgeElement ? bridgeElement.innerText.trim() : "";
    const hasErrorAlert = document.getElementById('login-error-alert') !== null;
    const masterValidated = sessionStorage.getItem('sicpro_master_key_ok');

    // Funciones globales asignadas a window para que el HTML pueda verlas (onclick)
    window.openStep1 = function() {
        document.getElementById('step-pass').style.display = 'flex';
    };

    window.closeAll = function() {
        sessionStorage.removeItem('sicpro_master_key_ok');
        document.getElementById('step-pass').style.display = 'none';
        document.getElementById('step-login').style.display = 'none';
    };

    window.checkKey = function() {
        const inputVal = document.getElementById('master-input').value;
        if (inputVal === dom_key) {
            sessionStorage.setItem('sicpro_master_key_ok', 'true');
            document.getElementById('step-pass').style.display = 'none';
            document.getElementById('step-login').style.display = 'flex';
        } else {
            const errMsg = document.getElementById('err-msg');
            if (errMsg) errMsg.style.display = 'block';
        }
    };

    // Auto-apertura si hay error de Odoo
    if (hasErrorAlert) {
        document.getElementById('step-pass').style.display = 'none';
        document.getElementById('step-login').style.display = 'flex';
    }
}

function initParticles() {
    const canvas = document.getElementById('canvas-particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let pts = [];
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    for (let i = 0; i < 50; i++) {
        pts.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            v: Math.random() * 0.5 + 0.2
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgba(113, 75, 103, 0.3)";
        pts.forEach(p => {
            p.y -= p.v;
            if (p.y < 0) p.y = canvas.height;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 1.5, 0, Math.PI * 2);
            ctx.fill();
        });
        requestAnimationFrame(draw);
    }
    draw();
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    initAdminLogic();
    initParticles();
});