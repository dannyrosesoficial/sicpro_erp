odoo.define('sicpro_modulo_plantilla_acceso.plantilla_acceso', function (require) {
	"use strict";

	window.onload = function () {
		// carga los roles y permisos especiales
		if (typeof (plantilla_acceso) != 'undefined') {

			// pasa a readonly los campos de la información del usuario
			Object.keys(plantilla_acceso).forEach(function (key, index) {
				if (key !== 'accion' && key !== 'roles')

				{
					let classTag = key.replace('_', '-');
					let input = $('input[name="' + classTag + '"]');
					input.val(he.decode(plantilla_acceso[key]));
					if (input.val()) {
						input.prop('readonly', true);
					}
				}
			});

			// muestra los roles actuales del usuario
			let roles_temp = he.decode(plantilla_acceso.roles);

			roles_temp = roles_temp.replaceAll('[', '');
			roles_temp = roles_temp.split('],');
			roles_temp[roles_temp.length - 1] = roles_temp[roles_temp.length - 1].replaceAll(']', '');

			roles_temp.forEach(function (rol) {
				let rol_arr = rol.split(',');

				if (rol_arr.length > 1) {
					$('select[name=' + rol_arr[0].trim() + '] option:contains(' + rol_arr[1].trim() + ')').attr('selected', '');
				}

			});
		}

		// agrega la fecha actual al solicitante y el que autoriza
		if ($('.plantilla-solicitud-rol input[name=solicitado-por-fecha]')[0]) {
			$('.plantilla-solicitud-rol input[name=solicitado-por-fecha]')[0].value = new Date().toISOString().substring(0, 10);
			$('.plantilla-solicitud-rol input[name=autorizado-por-fecha]')[0].value = new Date().toISOString().substring(0, 10);
		}

		$(document).on("click", ".plantilla-seleccion button.btn-modificar-usuario, .plantilla-seleccion button.btn-reiniciar-usuario, .plantilla-seleccion button.btn-eliminar-usuario, .plantilla-seleccion form button.btn-volver", function (event) {
			window.plantilla_seleccion_accion = false;
			switch (event.delegateTarget.activeElement.classList[2]) {
				case 'btn-modificar-usuario':
					plantilla_seleccion_accion = 'modificar';
					break;
				case 'btn-reiniciar-usuario':
					plantilla_seleccion_accion = 'reiniciar';
					break;
				case 'btn-archivar-usuario':
					plantilla_seleccion_accion = 'archivar';
					break;
				case 'btn-eliminar-usuario':
					plantilla_seleccion_accion = 'eliminar';
					break;
			}

			$('.plantilla-seleccion .o_hidden, .plantilla-seleccion .o_show').toggleClass("o_show o_hidden");
		});

		$(document).on("click", ".plantilla-seleccion form button.btn-confirmar-sap", function (event) {

			event.preventDefault();

			let form = $(".plantilla-seleccion form")[0];

			if (form.reportValidity()) {
				form.action = form.action + '?crear_consecutivo=&accion=' + plantilla_seleccion_accion +
					'&sap=' + form.getElementsByClassName('plantilla-acceso-seleccion-sap-input')[0].value;
				window.location.href = form.action;
			}
		});

		$(document).on("click", ".plantilla-seleccion button.btn-crear-usuario", function (event) {
			window.location.href = "/planilla_acceso/?crear_consecutivo=&accion=crear";
		});

		$(document).on("click", ".plantilla-solicitud-rol .abs button.btn-volver", function (event) {
			window.location.href = "/planilla_acceso/seleccion/";
		});

		$("select").off("change").on("change", function () {
			let val = $(this).val();

			$(this).find("option[value = " + val + "]").attr("selected", true);
		});

		// Imprime el documento a pdf
		$(document).on("click", ".plantilla-solicitud-rol button.btn-enviar", function (event) {

			event.preventDefault();

			let form = $(".plantilla-solicitud-rol form")[0];

			if (form.reportValidity()) {
				let window_element = $('.plantilla-solicitud-rol')[0];

				// console.log(window_element)

				let opt = {
					pagebreak: {mode: 'avoid-all'},
					jsPDF: {
						unit: "px",
						orientation: "p",
						format: [window_element.offsetHeight * 1.05, window_element.offsetWidth]
					},
				}

				let plantilla = $('.plantilla-solicitud-rol')[0];
				plantilla.style.backgroundColor = "white";
				$(plantilla).find('input[placeholder]').removeAttr('placeholder');
				$(plantilla).find('select option:contains(Elija)').text('');

				html2pdf().set(opt).from(plantilla).save('Planilla de Solicitud SICPRO ERP').then(function (result) {
					form.submit();
				});
			}

		});
	}

});
