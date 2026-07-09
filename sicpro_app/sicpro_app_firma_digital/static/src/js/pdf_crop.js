odoo.define('sicpro_app_firma_digital.recortando_imagen', function (require) {
	"use strict";

	var base_f = require('web.basic_fields');
	var imageWidget = base_f.FieldBinaryImage;
	var fieldRegistry = require('web.field_registry');
	var core = require('web.core');
	var bus = core.bus;
	var PDFCropWidget = require('sicpro_app_firma_digital.PDFCropWidget');


	// Creando widget sin barra de edición para usar el recortador sobre él 
	var imagen_firma_pdf_crop = imageWidget.extend({
		events: _.extend({}, imageWidget.prototype.events, {'click .img.img-fluid': 'add_bar',}),

		start: function () {
			var sup_ready = this._super.apply(this, arguments);
			sup_ready.then(() => {
				var self = this;
				var contador = 0;

				// Crear el widget barra de recortar cuando cargue la imagen del wizard
				this.$('img')[0].onload = function () {
					if (this.complete && typeof this.naturalWidth != "undefined" && this.naturalWidth != 0) {
						// Hacer que solo se realice la acción una única vez(cuando la imagen cargó por completo)
						if (contador < 1) {
							self.add_bar();
							contador = contador + 1;
						}

                        // agrego el valor del id de la imagen al input oculto para que la retorne el cropper
						// cuando obtenga las coordenadas de la firma
						$(document).ready(function()
							{
							$('input:text[name=pdf_cropper_value]').val(self.record.evalContext.id);
						})
					}
				}
			});
			return $.when(sup_ready);
		},

		//función para añadir la barra de recortar imagen, o sea para seleccionar el área de firma
		add_bar: async function () {
			var media = this.$('img')[0];
			if (!media.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
				await new Promise(r => setTimeout(r, 100));
				media = this.$('img')[0];
			}
			media.width = "1000";
			media.height = "500";
			media.dataset.originalSrc = media.getAttribute('src');
			media.dataset.initialSrc = media.getAttribute('src');
			new PDFCropWidget(this, media).appendTo(this.$el);
		},
	});

	fieldRegistry.add('firma_pdf_crop', imagen_firma_pdf_crop);
});
