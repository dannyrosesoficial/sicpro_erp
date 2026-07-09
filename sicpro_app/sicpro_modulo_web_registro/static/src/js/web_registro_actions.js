/**
 * SICPRO - Lógica de Registro de Usuarios
 * Versión compatible con Odoo 19
 */

// 1. VARIABLES GLOBALES
let currentUserData = null;
let rolesExternosAuto = []; // Configuración de sicpro.modulo.web.registro.roles

// 2. NAVEGACIÓN Y UTILIDADES
function goToStep(s) {
    const views = document.querySelectorAll('.page-view');
    views.forEach(view => view.classList.remove('active'));

    const target = document.getElementById('step' + s);
    if (target) target.classList.add('active');

    const indicators = document.querySelectorAll('.step-indicator');
    indicators.forEach((ind, idx) => {
        ind.classList.toggle('active', (idx + 1) <= s);
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showModal(icon, title, msg) {
    const mIcon = document.getElementById('modalIcon');
    const mTitle = document.getElementById('modalTitle');
    const mMsg = document.getElementById('modalMessage');
    const mAlert = document.getElementById('modalAlert');

    if (mIcon) mIcon.innerText = icon;
    if (mTitle) mTitle.innerText = title;
    if (mMsg) mMsg.innerText = msg;
    if (mAlert) mAlert.classList.add('active');
}

function closeModal() {
    const mAlert = document.getElementById('modalAlert');
    if (mAlert) mAlert.classList.remove('active');
}

// 3. VALIDACIÓN UNIVERSAL
function validateRequiredFields() {
    const accion = document.getElementById('hidden_solicitud').value;
    const tipoUsuario = document.getElementById('f_tipo').value;

    const requiredNames = [
        'nombre', 'correo', 'plaza', 'tipo_usuario', 'carnet', 'nivel',
        'cargo', 'area', 'uo', 'contacto', 'detalles_uso_sistema',
        'nombre_jefe_inmediato', 'cargo_jefe_inmediato', 'uo_jefe_inmediato', 'telefono_jefe_inmediato',
        'nombre_director', 'cargo_director', 'uo_director', 'telefono_director'
    ];

    let hasError = false;
    let firstMissingField = null;

    requiredNames.forEach(name => {
        const field = document.querySelector(`[name="${name}"]`);
        if (field && !field.disabled && field.style.display !== 'none') {
            if (field.value.trim() === '') {
                hasError = true;
                field.style.border = "1px solid #ef4444";
                if (!firstMissingField) firstMissingField = field;
            } else {
                field.style.border = "";
            }
        }
    });

    if (hasError) {
        showModal('⚠️', 'Campos Incompletos', 'Por favor, complete todos los campos obligatorios resaltados.');
        if (firstMissingField) firstMissingField.focus();
        return false;
    }

    // Validación de roles mínimos (excepto externos o bajas)
    if (accion !== 'eliminar' && accion !== 'reiniciar' && tipoUsuario !== 'externo') {
        let rolesAplicacion = 0;
        const selectsRoles = document.querySelectorAll('#step3 select:not([name="nivel"])');
        selectsRoles.forEach(sel => {
            if (sel.value !== "") rolesAplicacion++;
        });

        if (rolesAplicacion < 2) {
            showModal('⚠️', 'Roles Insuficientes', 'Debe seleccionar al menos 2 Roles de Aplicación.');
            return false;
        }
    }

    // Validación de Carnet de Identidad (Cuba)
    const ciField = document.getElementById('f_ci');
    const ci = ciField ? ciField.value : "";
    if (ci.length !== 11 || isNaN(ci)) {
        showModal('⚠️', 'Carnet Inválido', 'El Carnet debe tener exactamente 11 dígitos numéricos.');
        if (ciField) ciField.focus();
        return false;
    }

    return true;
}

// 4. BÚSQUEDA (CON VALIDACIÓN LDAP/ODOO Y PROTECCIÓN DE ID)
async function searchUser(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }

    const inputNombre = document.getElementById('s_nombre');
    const inputCorreo = document.getElementById('s_correo');
    const inputId = document.getElementById('s_id');
    const inputTipo = document.getElementById('s_tipo');

    // Validación campos vacíos
    if (!inputNombre.value.trim() || !inputCorreo.value.trim() || !inputId.value.trim() || !inputTipo.value) {
        showModal('⚠️', 'Atención', 'Todos los campos de búsqueda son obligatorios.');
        return false;
    }

    // Validación ID Solo Números (Segunda capa)
    const regexSoloNumeros = /^[0-9]+$/;
    if (!regexSoloNumeros.test(inputId.value.trim())) {
        showModal('⚠️', 'ID Inválido', 'El ID del trabajador debe contener solo números.');
        inputId.focus();
        return false;
    }

    document.body.style.cursor = 'wait';
    try {
        const response = await fetch('/sicpro/get_user_info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                params: { correo: inputCorreo.value.trim(), tipo_usuario: inputTipo.value }
            })
        });

        const res = await response.json();
        if (res.result && res.result.status === 'success') {
            const data = res.result.data;

            // VALIDACIÓN CRÍTICA: Bloqueo si no existe en ninguna fuente
            if (!data.existe && (!data.datos || Object.keys(data.datos).length === 0)) {
                showModal('❌', 'Usuario no encontrado', 'El correo no existe en Odoo ni en el Directorio Activo (LDAP).');
                return false;
            }

            currentUserData = data.datos || {};
            currentUserData.tipo_seleccionado = inputTipo.value;
            currentUserData.correo_ingresado = inputCorreo.value.trim();
            currentUserData.id_ingresado = inputId.value;
            currentUserData.nombre_ingresado = inputNombre.value;
            currentUserData.roles_internos = data.roles_internos || [];
            currentUserData.roles_especiales = data.roles_especiales || [];
            currentUserData.archivado = data.archivado || false;
            currentUserData.existe = data.existe || false;

            rolesExternosAuto = data.roles_externos_auto || [];

            // Resumen dinámico
            document.getElementById('userSummary').innerHTML = `
                <p><strong>Nombre:</strong> <span>${(data.existe || data.datos.nombre_apellidos) ? data.datos.nombre_apellidos : inputNombre.value}</span></p>
                <p><strong>ID/Plaza:</strong> <span>${(data.existe || data.datos.codigo_sap) ? data.datos.codigo_sap : inputId.value}</span></p>
                <p><strong>Tipo de Usuario:</strong> <span style="text-transform: capitalize; color: #714B67; font-weight: bold;">${inputTipo.value}</span></p>
                <p><strong>Estado:</strong> <span>${data.existe ? (data.archivado ? 'Archivado (Requiere Reinicio)' : 'Activo') : 'Nuevo Ingreso (LDAP)'}</span></p>
            `;

            // Visibilidad de botones según estado
            document.getElementById('btnCreate').style.display = (!data.existe) ? 'inline-flex' : 'none';
            document.getElementById('id_btn_reiniciar').style.display = (data.existe && data.archivado) ? 'inline-flex' : 'none';
            document.getElementById('btnModify').style.display = (data.existe && !data.archivado) ? 'inline-flex' : 'none';
            document.getElementById('btnDelete').style.display = (data.existe && !data.archivado) ? 'inline-flex' : 'none';

            goToStep(2);
        } else {
            showModal('❌', 'Error', res.result.message || 'Error al consultar la información.');
        }
    } catch (err) {
        showModal('⚠️', 'Error', 'Fallo de conexión con el servidor.');
    } finally {
        document.body.style.cursor = 'default';
    }
    return false;
}

// 5. CONFIGURACIÓN DE ACCIÓN
function seleccionarAccion(accion) {
    const inputSolicitud = document.getElementById('hidden_solicitud');
    if (inputSolicitud) inputSolicitud.value = accion;

    const campoFundamentacion = document.querySelector('[name="detalles_uso_sistema"]');
    const tipoUsuario = currentUserData.tipo_seleccionado;

    prellenarDatosFormulario();
    campoFundamentacion.readOnly = false;
    campoFundamentacion.value = '';

    limpiarRolesUI();

    if (currentUserData.existe) {
        cargarRolesEnUI(currentUserData.roles_internos, currentUserData.roles_especiales);
    }
    else if (accion === 'crear' && tipoUsuario === 'interno') {
        if (rolesExternosAuto && rolesExternosAuto.length > 0) {
            rolesExternosAuto.forEach(conf => {
                if (conf.default_rol) {
                    const select = document.querySelector(`select[name="${conf.app_name}"]`);
                    if (select) select.value = conf.default_rol;
                }
            });
        }
    }

    // Reglas de bloqueo de UI según acción
    if (accion === 'reiniciar' || accion === 'eliminar') {
        bloquearSeccionRoles(true);
        campoFundamentacion.value = accion === 'reiniciar' ? 'Se solicita el reinicio del usuario.' : 'Se solicita la baja por: ';
        if(accion === 'reiniciar') campoFundamentacion.readOnly = true;
    }
    else if (tipoUsuario === 'externo') {
        bloquearSelectsRoles(true);
        if (rolesExternosAuto && rolesExternosAuto.length > 0) {
            rolesExternosAuto.forEach(conf => {
                if (conf.automatizar_usuario_externo === true) {
                    conf.roles_list.forEach(rolObj => {
                        const select = document.querySelector(`select[name="${rolObj.app}"]`);
                        if (select) select.disabled = false;
                    });
                }
            });
        }
        bloquearCheckboxes(false);
    }
    else {
        bloquearSeccionRoles(false);
    }

    const badge = document.getElementById('formModeBadge');
    if (badge) {
        badge.innerText = accion.toUpperCase();
        badge.className = 'badge ' + (accion === 'eliminar' ? 'bg-danger' : (accion === 'reiniciar' ? 'bg-warning' : 'bg-primary'));
    }

    goToStep(3);
}

// 6. ENVÍO FINAL
async function survey_submit(e) {
    if (e) e.preventDefault();
    if (!validateRequiredFields()) return;

    const form = document.getElementById('mainForm');
    const vals_data = {};
    const elements = form.querySelectorAll('input, select, textarea');

    elements.forEach(el => {
        if (el.name && el.type !== 'checkbox' && el.type !== 'submit') {
            vals_data[el.name] = el.value;
        }
    });

    const especiales = [];
    document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked').forEach(ch => {
        especiales.push(ch.name);
    });
    vals_data['permisos_especiales_lista'] = especiales;

    document.body.style.cursor = 'wait';
    try {
        const response = await fetch('/sicpro/registro_submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ params: { vals: vals_data } })
        });
        const res = await response.json();

        if (res.result && res.result.status === 'success') {
            showModal('✅', 'Éxito', 'Solicitud enviada correctamente. Consecutivo: ' + res.result.consecutivo);
            setTimeout(() => { window.location.href = "/sicpro/inicio"; }, 2500);
        } else {
            showModal('❌', 'Error', res.result.message);
        }
    } catch (err) {
        showModal('⚠️', 'Error', 'Error al procesar la solicitud.');
    } finally {
        document.body.style.cursor = 'default';
    }
}

// --- FUNCIONES DE APOYO ---
function prellenarDatosFormulario() {
    const d = currentUserData;
    if (!d) return;
    const fields = {
        'f_nombre': (d.nombre_apellidos) ? d.nombre_apellidos : d.nombre_ingresado,
        'f_correo': d.correo_ingresado,
        'f_id': (d.codigo_sap) ? d.codigo_sap : d.id_ingresado,
        'f_tipo': d.tipo_seleccionado,
        'f_cargo': d.cargo || '',
        'f_area': d.area || '',
        'f_uo': d.uo || ''
    };
    for (let id in fields) {
        const el = document.getElementById(id);
        if (el) el.value = fields[id];
    }
}

function limpiarRolesUI() {
    document.querySelectorAll('#step3 select:not([name="nivel"])').forEach(s => s.value = "");
    document.querySelectorAll('#step3 input[type="checkbox"]').forEach(c => c.checked = false);
}

function cargarRolesEnUI(internos, especiales) {
    if (internos) internos.forEach(r => {
        const select = document.querySelector(`select[name="${r.app}"]`);
        if (select) select.value = r.rol;
    });
    if (especiales) especiales.forEach(e => {
        const check = document.querySelector(`input[type="checkbox"][name="${e}"]`);
        if (check) check.checked = true;
    });
}

function bloquearSelectsRoles(estado) {
    document.querySelectorAll('#step3 select:not([name="nivel"])').forEach(s => s.disabled = estado);
}

function bloquearCheckboxes(estado) {
    document.querySelectorAll('#step3 input[type="checkbox"]').forEach(c => c.disabled = estado);
}

function bloquearSeccionRoles(estado) {
    bloquearSelectsRoles(estado);
    bloquearCheckboxes(estado);
    const sn = document.querySelector('select[name="nivel"]');
    if (sn) sn.disabled = false;
}

// --- INICIALIZACIÓN ---
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mainForm');
    if (form) form.onsubmit = survey_submit;

    const btnSearchUser = document.getElementById('btnSearchUser');
    if (btnSearchUser) btnSearchUser.onclick = searchUser;

    // Restricción de ID solo números en tiempo real
    const inputIdSearch = document.getElementById('s_id');
    if (inputIdSearch) {
        inputIdSearch.addEventListener('keypress', function(e) {
            if (e.which < 48 || e.which > 57) {
                e.preventDefault();
            }
        });
    }
});