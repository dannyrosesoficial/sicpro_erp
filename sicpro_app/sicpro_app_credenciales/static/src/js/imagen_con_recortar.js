odoo.define('sicpro_app_credenciales.imagen_con_recortar', function (require) {
	"use strict";

	// Importando las Cosas para crear el widget
	var base_f = require('web.basic_fields');
	var imageWidget = base_f.FieldBinaryImage;
	var fieldRegistry = require('web.field_registry');

	var core = require('web.core');
	var qweb = core.qweb;
	var utils = require('web.utils');

	var bus = core.bus;
	
	// Widget de imagen con botón de recortar agregado
	var imagen_con_recortar = imageWidget.extend({
		template: 'ImagenConBotonDeRecortarTemplate',
		events: _.extend({}, imageWidget.prototype.events, {
			'click .o_crop_file_button': 'btn_recortar_action',
		}),

		renderizar_imagen_actualizada: async function(imagen) {
			//en vez de cargar la imagen de la base de datos la asignaremos directamente al campo
			await new Promise(r => setTimeout(r,300));
			this._setValue(imagen);
		},

		// Hacer click en el botón invisible para abrir el modal desde python y así activar el campo de 'active_id'
		btn_recortar_action: function(){
			//Crear el evento para actualizar la imagen al terminar de recortar sin tener que recargar la imagen
			bus.on('actualizar_imagen', this, function(imagen) {
				this.renderizar_imagen_actualizada(imagen);
			});

			$('#boton_recortar_imagen').click();


		},

		// Reimplementando el renderizador original del fieldBinaryImage para que renderice la imagen recortada con el template creado
		_render: function () {
        var self = this;
        var url = this.placeholder;
        if (this.value) {
            if (!utils.is_bin_size(this.value)) {
                // Use magic-word technique for detecting image type
                url = 'data:image/' + (this.file_type_magic_word[this.value[0]] || 'png') + ';base64,' + this.value;
            } else {
                var field = this.nodeOptions.preview_image || this.name;
                var unique = this.recordData.__last_update;
                url = this._getImageUrl(this.model, this.res_id, field, unique);
            }
        }
        var $img = $(qweb.render("ImagenConBotonDeRecortarTemplate-img", {widget: this, url: url}));
        // override css size attributes (could have been defined in css files)
        // if specified on the widget
        var width = this.nodeOptions.size ? this.nodeOptions.size[0] : this.attrs.width;
        var height = this.nodeOptions.size ? this.nodeOptions.size[1] : this.attrs.height;
        if (width) {
            $img.attr('width', width);
            $img.css('max-width', width + 'px');
        }
        if (height) {
            $img.attr('height', height);
            $img.css('max-height', height + 'px');
        }
        this.$('> img').remove();
        this.$el.prepend($img);

        $img.one('error', function () {
            $img.attr('src', self.placeholder);
            self.displayNotification({ message: _t("Could not display the selected image"), type: 'danger' });
        });

        return this._super.apply(this, arguments);
    },


	});

	fieldRegistry.add('imagen_con_recortar', imagen_con_recortar);

	return imagen_con_recortar;

});
