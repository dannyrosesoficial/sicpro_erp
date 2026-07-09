/**
 * SICPRO Countdown & Sync System
 * Developer: Danny Rose's 🌹
 */

function iniciarContador() {
    const dom_start = document.getElementById('os_date').innerText.trim();
    const dom_dur = document.getElementById('om_time').innerText.trim();

    function parseOdooDateUTC(s) {
        const p = s.match(/\d+/g);
        if (p && p.length >= 3) {
            return new Date(Date.UTC(p[0], p[1] - 1, p[2], p[3] || 0, p[4] || 0, p[5] || 0)).getTime();
        }
        return Date.now();
    }

    function parseDurationToMs(s) {
        const p = s.split(':');
        const h = parseInt(p[0]) || 0;
        const m = parseInt(p[1]) || 0;
        const sec = parseInt(p[2]) || 0;
        const total = ((h * 3600) + (m * 60) + sec) * 1000;
        return total > 0 ? total : 1800000; // 30 min por defecto
    }

    const startMs = parseOdooDateUTC(dom_start);
    const durationMs = parseDurationToMs(dom_dur);
    const endMs = startMs + durationMs;

    const timerInterval = setInterval(function() {
        const now = Date.now();
        const remaining = endMs - now;
        const elapsed = now - startMs;

        // Cálculo del porcentaje basado en el tiempo transcurrido
        let rawPercent = (elapsed / durationMs) * 100;

        if (remaining <= 0) {
            document.getElementById('countdown-timer').innerHTML = "00:00:00";
            document.getElementById('sync-percent').innerHTML = "100.0%";
            document.getElementById('status-text').innerHTML = "OPERACIONAL";
            clearInterval(timerInterval);
            return;
        }

        // Formateo del cronómetro (HH:MM:SS)
        const h = Math.floor(remaining / 3600000);
        const m = Math.floor((remaining % 3600000) / 60000);
        const sec = Math.floor((remaining % 60000) / 1000);

        document.getElementById('countdown-timer').innerHTML =
            String(h).padStart(2, '0') + ":" +
            String(m).padStart(2, '0') + ":" +
            String(sec).padStart(2, '0');

        // Actualización del porcentaje visual
        let displayPercent = rawPercent > 0 ? rawPercent.toFixed(1) : "0.1";
        if (rawPercent >= 100) displayPercent = "99.9"; // Evita mostrar 100% antes de terminar

        document.getElementById('sync-percent').innerHTML = displayPercent + "%";

    }, 1000);
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', iniciarContador);