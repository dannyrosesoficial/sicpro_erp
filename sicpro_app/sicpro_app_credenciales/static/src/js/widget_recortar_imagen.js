/** @odoo-module **/

import { ImageField } from "@web/views/fields/image/image_field";
import { registry } from "@web/core/registry";
import { onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class ImagenSinBarraDeEdicion extends ImageField {
    static template = "sicpro_app_credenciales.ImagenSinBarraTemplate";

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");

        // Danny: Referencias directas para evitar problemas de estado 🌹
        this.imageRef = useRef("image");
        this.msgRef = useRef("processing_msg");
        this.saveBtnRef = useRef("save_btn");

        onMounted(() => {
            // Danny: Un solo timeout para dejar que el modal se dibuje 🌹
            setTimeout(() => {
                this._initializeCropper();
            }, 500);
        });

        onWillUnmount(() => {
            const imgEl = this.imageRef.el;
            if (imgEl && imgEl.cropperInstance) {
                imgEl.cropperInstance.destroy();
            }
        });
    }

    _getRecordId() {
        return this.props.record.resId ||
               this.props.record.data?.id ||
               this.props.record.context?.active_id ||
               this.env.action_data?.context?.active_id;
    }

    async _initializeCropper() {
        const imgEl = this.imageRef.el;
        if (!imgEl) return;

        const resId = this._getRecordId();
        const model = this.props.record.resModel;
        const fieldName = this.props.name;

        // Danny: Cargamos la imagen base antes de activar la rejilla 🌹
        try {
            if (resId && typeof resId === 'number') {
                const data = await this.orm.read(model, [resId], [fieldName]);
                if (data && data[0] && data[0][fieldName]) {
                    imgEl.src = `data:image/png;base64,${data[0][fieldName]}`;
                } else {
                    imgEl.src = this.getUrl(fieldName);
                }
            } else {
                imgEl.src = this.getUrl(fieldName);
            }
        } catch (e) {
            imgEl.src = this.getUrl(fieldName);
        }

        imgEl.onload = () => {
            if (imgEl.cropperInstance) imgEl.cropperInstance.destroy();
            imgEl.cropperInstance = new window.Cropper(imgEl, {
                viewMode: 1,
                dragMode: 'move',
                autoCropArea: 0.8,
                aspectRatio: 1,
                responsive: true,
                checkOrientation: false,
                ready: function () {
                    this.cropper.crop();
                },
            });
        };
    }

    async saveCroppedImage() {
        const imgEl = this.imageRef.el;
        if (!imgEl || !imgEl.cropperInstance) return;

        const recordId = this._getRecordId();
        if (!recordId) return;

        // Danny: Feedback visual con estructura blindada para que el texto NO gire 🌹
        if (this.msgRef.el) this.msgRef.el.classList.remove('d-none');

        if (this.saveBtnRef.el) {
            this.saveBtnRef.el.disabled = true;
            // Danny: Usamos etiquetas separadas para aislar la animación 🌹
            this.saveBtnRef.el.innerHTML = `
                <span class="d-flex align-items-center justify-content-center">
                    <i class="fa fa-refresh fa-spin me-2" style="display: inline-block;"></i>
                    <span style="display: inline-block; transform: none !important;">Guardando...</span>
                </span>
            `;
        }

        try {
            await new Promise(r => setTimeout(r, 150));

            const canvas = imgEl.cropperInstance.getCroppedCanvas({
                width: 1024,
                height: 1024,
                imageSmoothingQuality: 'high',
            });

            const base64Data = canvas.toDataURL('image/png').split(',')[1];

            await this.orm.write('sicpro.app.credenciales', [recordId], {
                credencial_image_1920: base64Data
            });

            this.env.bus.trigger('actualizar_imagen', { imagen: base64Data });
            this.notification.add(_t("¡Guardado! 🌹"), { type: "success" });
            this.action.doAction({ type: 'ir.actions.act_window_close' });

        } catch (error) {
            if (this.msgRef.el) this.msgRef.el.classList.add('d-none');
            if (this.saveBtnRef.el) {
                this.saveBtnRef.el.disabled = false;
                this.saveBtnRef.el.innerHTML = '<i class="fa fa-save me-2"/> Guardar';
            }
            this.notification.add(_t("Error: " + error.message), { type: "danger" });
        }
    }

    onAction(type, value) {
        const imgEl = this.imageRef.el;
        if (imgEl && imgEl.cropperInstance && type === 'ratio') {
            imgEl.cropperInstance.setAspectRatio(value === '1/1' ? 1 : NaN);
        }
    }
}

registry.category("fields").add("recortar_imagen", {
    component: ImagenSinBarraDeEdicion,
    supportedTypes: ["binary"],
});