odoo.define('sicpro_app_credenciales.recortando_imagen', function (require) {
	"use strict";

	var base_f = require('web.basic_fields');
	var imageWidget = base_f.FieldBinaryImage;
	var fieldRegistry = require('web.field_registry');
	var core = require('web.core');
	var bus = core.bus;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	// Importando las Cosas originales de web_editor para crear el widget

	var ImageCropWidget = require('sicpro_app_credenciales.ImageCropWidget');

	var {applyModifications, cropperDataFields, activateCropper, loadImage, loadImageInfo} = require('sicpro_app_credenciales.image_processing');

	// Haciendo mínimos cambios al ImageCropWidget original
	var RecortadorDeImagenModificado = ImageCropWidget.extend({
		 /**
     * @override
     */
     async willStart() {
     	await this._super.apply(this, arguments);
     	this.originalSrc = this.media.dataset.originalSrc;
     	this.originalId = this.media.dataset.originalId;
     	return;
     },
     async start() {
     	if (this.uncroppable) {
     		this.displayNotification({
     			type: 'warning',
     			title: _t("Esta imagen es una imagen externa."),
     			message: _t("This type of image is not supported for cropping.<br/>If you want to crop it, please first download it from the original source and upload it in Odoo."),
     		});
     		return this.destroy();
     	}
     	const _super = this._super.bind(this);
     	const $cropperWrapper = this.$('.o_we_cropper_wrapper');

        // Replacing the src with the original's so that the layout is correct.
        await loadImage(this.originalSrc, this.media);
        this.$cropperImage = this.$('.o_we_cropper_img');
        const cropperImage = this.$cropperImage[0];
        [cropperImage.style.width, cropperImage.style.height] = [this.$media.width() + 'px', this.$media.height() + 'px'];

        // Overlaying the cropper image over the real image
        const offset = this.$media.offset();
        offset.left += parseInt(this.$media.css('padding-left'));
        offset.top += parseInt(this.$media.css('padding-right'));
        $cropperWrapper.offset(offset);

        await loadImage(this.originalSrc, cropperImage);
        await activateCropper(cropperImage, this.aspectRatios[this.aspectRatio].value, this.media.dataset);

        // We use capture so that the handler is called before other editor handlers
        // like save, such that we can restore the src before a save.
        return _super(...arguments);
    },
    /**
     * @override
     */
     destroy() {
     	if (this.$cropperImage) {
     		this.$cropperImage.cropper('destroy');
     	}
     	this.media.setAttribute('src', this.initialSrc);
     	this.$media.trigger('image_cropper_destroyed');
     	return this._super(...arguments);
     },
 });

// Aquí termina el código del recortador original(el que venía en web editor).
// Fueron llamados los métodos anteriores en específico para remover el evento que hacía desaparecer el widget cuando se clickeaba fuera de la imagen
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	// Creando widget sin barra de edición para usar el recortador sobre él 
	var imagen_sin_barra_de_edicion = imageWidget.extend({
		template: 'ImagenSinBarraTemplate',
		events: _.extend({}, imageWidget.prototype.events, {
			'click .img.img-fluid': 'add_bar',
		}),

		start: function(){
			var sup_ready = this._super.apply(this,arguments);

			sup_ready.then(() => {
				var self = this;
				var contador = 0;

				// Crear el widget barra de recortar cuando cargue la imagen del modal
				this.$('img')[0].onload = function () {
					if(this.complete && typeof this.naturalWidth != "undefined" && this.naturalWidth != 0){
						// Hacer que solo se realice la acción una única vez(cuando la imagen cargó por completo)
						if(contador < 1){
							self.add_bar();
							contador = contador + 1;
						}

						// Crear un evento de click en el botón de salvar para llevar la imagen recortada al record 
						if($('#credenciales-recortaŕ-y-guardar')[0]){
							$('#credenciales-recortaŕ-y-guardar')[0].onclick = async function () {
									var cropped_src = $('.modal-content img')[0].src;
									cropped_src = cropped_src.replace("data:image/png;base64,","");

									var record_a_cambiar = self.record.evalContext.active_id;
									self._rpc({
										model: 'sicpro.app.credenciales',
										method: 'update',
										args: [record_a_cambiar, {credencial_image_1920: cropped_src}],
									}).catch((error) => {
										console.log(error);
									});
									
									//Actualizar la imagen de el formulario al cerrar el modal
									bus.trigger('actualizar_imagen', cropped_src);


							}

						}
					}

				}	
			});
			

			return $.when(sup_ready);
		},

		//función para añadir la barra de recortar imagen, al cargar la imagen o al hacer click sobre ella cuando no existe barra porque ya se ha recortado.
		add_bar: async function () {
			var media = this.$('img')[0];
			if(!media.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0){
				await new Promise(r => setTimeout(r,100));
				media = this.$('img')[0];
			}
			media.width = "200";
			media.height = "200";
			media.dataset.originalSrc = media.getAttribute('src');
			media.dataset.initialSrc = media.getAttribute('src');
			new RecortadorDeImagenModificado(this, media).appendTo(this.$el);
		},
	});
	
	fieldRegistry.add('imagen_sin_barra', imagen_sin_barra_de_edicion);

});
