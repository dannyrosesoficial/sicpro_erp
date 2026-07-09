odoo.define('sicpro_app_firma_digital.PDFCropWidget', function (require) {
    'use strict';

    const core = require('web.core');
    const Widget = require('web.Widget');
    const {applyModifications, cropperDataFields, activateCropper, loadImage, loadImageInfo} = require('sicpro_app_firma_digital.image_processing');

    const _t = core._t;

    const ImageCropWidget = Widget.extend({
        template: ['sicpro.firma.digital.crop.original'],
        events: {'click.crop_options [data-action]': '_onCropOptionClick',},

        /**
         * @constructor
         */
        init(parent, media) {
            this._super(...arguments);
            this.media = media;
            this.$media = $(media);
            // Necesario para editores en iframes.
            this.document = media.ownerDocument;
            // clave: identificador de proporción, etiqueta: mostrada al usuario, valor: utilizado por cropper lib
            this.aspectRatios = {
                "0/0": {label: _t("Flexible"), value: 0},
                "16/9": {label: "16:9", value: 16 / 9},
                "4/3": {label: "4:3", value: 4 / 3},
                "1/1": {label: "1:1", value: 1},
                "2/3": {label: "2:3", value: 2 / 3},
            };
            const src = this.media.getAttribute('src');
            const data = Object.assign({}, media.dataset);
            this.initialSrc = src;
            this.aspectRatio = data.aspectRatio || "0/0";
            this.mimetype = data.mimetype || src.endsWith('.png') ? 'image/png' : 'image/jpeg';
        },
        /**
         * @override
         */
        async willStart() {
            await this._super.apply(this, arguments);
            this.originalSrc = this.media.dataset.originalSrc;
            this.originalId = this.media.dataset.originalId;

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

            var sup_ready = this._super.apply(this,arguments);

            sup_ready.then(() => {
				var self = this;
				// Crear un evento de click en el botón de guardar para enviar las coordenadas del pdf
                    if ($('#enviar_cropper_pdf')[0]) {
                        $('#enviar_cropper_pdf')[0].onclick = async function () {
                            var imagen_id = $('input:text[name=pdf_cropper_value]').val();
                            var cropper_pdf = self.cropper_pdf();
                            Promise.all([cropper_pdf]).then((values) => {
                                self._rpc({
                                    model: 'sicpro.app.firma.documentos.imagenes',
                                    method: 'actualizar_coordenadas',
                                    args: [{imagen_id},values],
                                }).catch((error) => {
                                    console.log(error);
                                });
                            });
                        }
                    }
			});

            const _super = this._super.bind(this);
            const $cropperWrapper = this.$('.o_we_cropper_wrapper');

            // Reemplazar el src con el original para que el diseño sea correcto.
            await loadImage(this.originalSrc, this.media);
            this.$cropperImage = this.$('.o_we_cropper_img');
            const cropperImage = this.$cropperImage[0];

            [cropperImage.style.width, cropperImage.style.height] = [this.$media.width() + 'px', this.$media.height() + 'px'];

            // Superponer la imagen del recortador sobre la imagen real
            const offset = this.$media.offset();
            offset.left += parseInt(this.$media.css('padding-left'));
            offset.top += parseInt(this.$media.css('padding-right'));
            $cropperWrapper.offset(offset);



            await loadImage(this.originalSrc, cropperImage);
            await activateCropper(cropperImage, this.aspectRatios[this.aspectRatio].value, this.media.dataset);

            // Usamos captura para que el controlador sea llamado antes que otros controladores del editor.
            // como guardar, de modo que podamos restaurar el src antes de guardar.
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


        // Guardar coordenadas
        async _save(cropped = true) {
            // Mark the media for later creation of cropped attachment
            this.media.classList.add('o_modified_image_to_save');
            var lista=[];
            [...cropperDataFields, 'aspectRatio'].forEach(attr => {
                delete this.media.dataset[attr];
                const value = this._getAttributeValue(attr);
                if (value) {
                    lista.push(value);
                }
            });
            return lista
        },


        cropper_pdf: function () {
            return this._save()
        },


        // Devuelve el valor de un atributo para guardar.
        _getAttributeValue(attr) {
            if (cropperDataFields.includes(attr)) {
                return this.$cropperImage.cropper('getData')[attr];
            }
            return this[attr];
        },


        // seleccionar area de firma
        _onCropOptionClick(ev) {
            const {action, value, scaleDirection} = ev.currentTarget.dataset;
            switch (action) {
                case 'apply':
                    return this._save();
            }
        },

    });

    return ImageCropWidget;
});
