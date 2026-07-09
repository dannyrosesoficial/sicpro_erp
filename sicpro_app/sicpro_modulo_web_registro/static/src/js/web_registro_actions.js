odoo.define('sicpro_modulo_web_registro.web_plantilla_registro', function (require) {
	"use strict";

	window.onload = function () {

		// Inicio del código del templete: web_plantilla_registro
		// verifica si el usuario no existe para enviar el aviso
		let estado_usuario = false;
		if (typeof (ejecutar_aviso) != 'undefined') {
			if (ejecutar_aviso.ejecutar === 'usuario_ldap_false') {
				Swal.fire({
					icon: 'info',
					title: 'Oops...',
					text: 'El usuario no esta registrado en el ldap Empresarial!',
					footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
				})
				return;
			}
		}

		// Compruebo que los campos esten llenos correctamente
		let chequeo_campos = false;
		let chequeo_select_cheq = false;
		let tipo_usuario = false;
		$('#signup').click(function (event) {
			event.preventDefault();

			// Compruebo que existan datos en los campos de nombre, correo y #plaza
			const correo = $('#email').val();
			chequeo_campos = $('#name').val().length > 0;
			chequeo_campos = correo.length > 0;
			chequeo_campos = $('#plaza').val().length > 0;
			if (chequeo_campos === true) {
				// compruebo este seleccionado algún tipo de usuario
				tipo_usuario = $('#tipo_usuario').val();
				if (tipo_usuario === "0") {
					chequeo_select_cheq = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe seleccionar el tipo de usuario que desea crear!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;

				} else {
					chequeo_select_cheq = true;
				}


				// compruebo que esta activo el checkbox de visto los términos de servicios
				if ($('input[name=agree-term]').is(':checked')) {
					chequeo_select_cheq = true;
				} else {
					chequeo_select_cheq = false;
					// Modal de alerta
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe aceptar los términos y condiciones del servicio SICPRO!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return
				}

			} else {
				// Modal de alerta
				Swal.fire({
					icon: 'error',
					title: 'Oops...',
					text: 'Le faltan datos requeridos por completar!',
					footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
				})
				return;
			}

			// compruebo si todos los campos esten llenos correctamente y redirecciono
			if (chequeo_select_cheq === true) {
				// redirecciono
				window.location.href = '/web/registro_selector/' + '?correo=' + correo + '&tipo=' + tipo_usuario;
			}

		});
		// Fin del código del templete: web_plantilla_registro

		// Inicio del código del templete: web_plantilla_registro_selector
		// valido los botones de (crear/modificar/reiniciar/eliminar) y redirecciono a la pagina especifica
		$(document).on("click", "button.btn-crear, button.btn-modificar, button.btn-reiniciar, button.btn-eliminar", function (event) {
			let solicitud_user = false;
			let correo_user = false;
			let tipo_user = false;
			let estado_user = false;
			switch (event.delegateTarget.activeElement.classList[3]) {
				case 'btn-crear':
					solicitud_user = 'crear';
					break;
				case 'btn-modificar':
					solicitud_user = 'modificar';
					break;
				case 'btn-reiniciar':
					solicitud_user = 'reiniciar';
					break;
				case 'btn-eliminar':
					solicitud_user = 'eliminar';
					break;
			}

			// busco el valor del correo para pasarlo a la próxima pagina
			if (typeof (correo_trabajador) != 'undefined') {
				correo_user = correo_trabajador.correo;
				tipo_user = correo_trabajador.tipo;
				estado_user = correo_trabajador.estado_usuario;
			}

			// redirecciono
			window.location.href = '/web/registro_planilla/' + '?correo=' + correo_user + '&solicitud='
				+ solicitud_user + '&tipo=' + tipo_user + '&estado=' + estado_user;
		});
		// Fin del código del templete: web_plantilla_registro_selector

		// Inicio del código del templete: web_plantilla_registro_planilla
		// verifico que el templete sea el correcto para actualizar los roles
		// al iniciar oculto el btn de enviar la solicitud
		$('#enviar').hide();
		// compruebo que exista el objeto: data_solicitud
		if (typeof (data_solicitud) != 'undefined') {
			if (data_solicitud.templete === 'planilla_roles'){
				let tipo_users = $('#tipo_usuario').val()
				let tipo_solicitud = data_solicitud.solicitud

				// ejecuto si es un usuario externo
				if (tipo_users === 'externo'){
					let roles_externos = he.decode(data_solicitud.roles_externos);
					roles_externos = roles_externos.replaceAll('[', '');
					roles_externos = roles_externos.split('],');
					roles_externos[roles_externos.length - 1] = roles_externos[roles_externos.length - 1].replaceAll(']', '');

					roles_externos.forEach(function (rol) {
						let rol_arr = rol.split(',');
						if (rol_arr.length > 1) {
							$('select[name=' + rol_arr[0].trim() + '] option:contains(' + rol_arr[1].trim() + ')').attr('selected', '');
						 }
					});
				}
				else{
					// ejecuto si es un usuario interno
					if (tipo_solicitud === 'modificar' || tipo_solicitud === 'reiniciar' || tipo_solicitud === 'eliminar'){
						// acción a ejecutar si la solicitud es para modificar, reiniciar o eliminar
						let roles_internos = he.decode(data_solicitud.roles_internos);
						roles_internos = roles_internos.replaceAll('[', '');
						roles_internos = roles_internos.split('],');
						roles_internos[roles_internos.length - 1] = roles_internos[roles_internos.length - 1].replaceAll(']', '');

						roles_internos.forEach(function (rol) {
							let rol_arr = rol.split(',');
							if (rol_arr.length > 1) {
								$('select[name=' + rol_arr[0].trim() + '] option:contains(' + rol_arr[1].trim() + ')').attr('selected', '');
							 }
						});
					}
				}
			}
		}

		// finalizo la solicitud de acceso
		$('#finish').click(function (event) {
			event.preventDefault();
			// Compruebo que existan datos en los campos de carnet, nivel escolar y contactos
			let chequear_campos = false;

			if (!($('#carnet').val().length > 0)) {
				chequear_campos = false;
				Swal.fire({
					icon: 'warning',
					title: 'Oops...',
					text: 'Para continuar debe agregar datos al campo de Carnet de Identidad!',
					footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
				})
				return;
			} else {
				chequear_campos = true;
			}

			let nivel_escolar = $('#nivel').val();
			if (nivel_escolar === "0") {
				chequear_campos = false;
				Swal.fire({
					icon: 'warning',
					title: 'Oops...',
					text: 'Para continuar debe agregar datos al campo de Nivel Escolar!',
					footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
				})
				return;
			} else {
				chequear_campos = true;
			}

			if (!($('#contacto').val().length > 0)) {
				chequear_campos = false;
				Swal.fire({
					icon: 'warning',
					title: 'Oops...',
					text: 'Para continuar debe agregar datos al campo de Teléfonos de Contactos!',
					footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
				})
				return;
			} else {
				chequear_campos = true;
			}

			let chequeo_esp_importar = $('input[name=importar]').is(':checked');
			let chequeo_esp_exportar_avazado = $('input[name=exportar_avanzado]').is(':checked');
			let chequeo_esp_multiproceso = $('input[name=multiprocesos]').is(':checked');
			if (chequeo_esp_importar === true || chequeo_esp_exportar_avazado === true || chequeo_esp_multiproceso === true) {
				if (!($('#detalles_permisos_especiales').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe fundamentar el motivo de la solicitud de accesos especiales!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;

				} else {
					chequear_campos = true;
				}
			}

			if (!($('#detalles_uso_sistema').val().length > 0)) {
				chequear_campos = false;
				Swal.fire({
					icon: 'warning',
					title: 'Oops...',
					text: 'Para continuar debe fundamentar el motivo de uso del sistema!',
					footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
				})
				return;
			} else {
				chequear_campos = true;
			}

			if (!(data_solicitud.solicitud === 'reiniciar')) {

				if (!($('#nombre_jefe_inmediato').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar el nombre y apellidos del jefe inmediato del trabajador!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

				if (!($('#cargo_jefe_inmediato').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar el cargo del jefe inmediato del trabajador!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

				if (!($('#uo_jefe_inmediato').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar la unidad organizativa del jefe inmediato del trabajador!!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

				if (!($('#telefono_jefe_inmediato').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar teléfono de contacto del jefe inmediato del trabajador!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

				if (!($('#nombre_director').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar el nombre y apellidos del director del trabajador!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

				if (!($('#cargo_director').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar el cargo del director del trabajador!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

				if (!($('#uo_director').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar la unidad organizativa del director del trabajador!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

				if (!($('#telefono_director').val().length > 0)) {
					chequear_campos = false;
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Para continuar debe agregar el teléfono de contacto del director del trabajador!',
						footer: '<a href="mailto:daniel.borrero@etecsa.cu">Contacto de soporte</a>'
					})
					return;
				} else {
					chequear_campos = true;
				}

			} else {
				chequear_campos = true;
			}

			// var $wizard = navigation.closest('.wizard-card');
			// compruebo si todos los campos esten llenos correctamente y redirecciono
			if (chequear_campos === true) {
                $('#finish').hide();
                $('#previous').hide();
                $('#enviar').show();
			}

		});
		// Fin del código del templete: web_plantilla_registro_planilla

	}
});
