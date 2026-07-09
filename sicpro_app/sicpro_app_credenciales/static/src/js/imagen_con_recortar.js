/** @odoo-module **/

import { ImageField } from "@web/views/fields/image/image_field";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { onWillUnmount } from "@odoo/owl";

export class ImagenConRecortar extends ImageField {
    static template = "sicpro_app_credenciales.ImagenConBotonDeRecortarTemplate";

    setup() {
        super.setup();
        this.action = useService("action");
        this.notification = useService("notification");

        // Usamos una función vinculada para poder removerla correctamente
        this.onUpdateHandler = this.onUpdate.bind(this);
        this.env.bus.addEventListener("actualizar_imagen", this.onUpdateHandler);

        onWillUnmount(() => {
            this.env.bus.removeEventListener("actualizar_imagen", this.onUpdateHandler);
        });
    }

    async onUpdate(ev) {
        if (ev.detail && ev.detail.imagen) {
            await this.renderizarImagenActualizada(ev.detail);
        }
    }

    async renderizarImagenActualizada(detail) {
        // Estado 5 es DESTROYED. Validamos antes de cualquier operación asíncrona.
        if (this.__owl__.status === 5) return;

        const { imagen } = detail;
        const record = this.props.record;

        try {
            // 1. Solo actualizamos el valor en el modelo de datos.
            // Odoo se encargará de marcar el registro como "sucio" (dirty).
            await record.update({ [this.props.name]: imagen });

            // 2. En lugar de manipular el DOM con querySelector (que causa el doble clic),
            // dejamos que el mecanismo nativo de Odoo guarde si es necesario.
            if (record.isDirty) {
                await record.save();
            }

            // 3. Notificamos al usuario del éxito
            this.notification.add("Imagen actualizada correctamente 🌹", {
                type: "success",
                sticky: false,
            });

        } catch (e) {
            // Si el error es porque el registro se destruyó durante el await, ignoramos.
            if (this.__owl__.status === 5) return;
            console.error("Error en Sincronización SICPRO 🌹:", e);
        }
    }

    async onCropButtonClicked() {
        const record = this.props.record;
        // resId puede ser virtual (NewId) si el registro no se ha guardado nunca
        const resId = record.resId || (typeof record.data.id === 'number' ? record.data.id : false);

        try {
            await this.action.doAction("sicpro_app_credenciales.action_wizard_recortar_imagen", {
                additionalContext: {
                    active_id: resId,
                    active_model: record.resModel,
                    active_field: this.props.name,
                },
                onClose: async () => {
                    // Simplemente recargamos el registro, OWL redibujará la imagen automáticamente
                    // eliminando la necesidad de manipular el SRC manualmente.
                    await record.load();
                },
            });
        } catch (error) {
            console.error("Error al abrir wizard en SICPRO 🌹:", error);
        }
    }

    // Método simplificado para el botón
    btnRecortarAction() {
        this.onCropButtonClicked();
    }
}

registry.category("fields").add("imagen_con_recortar", {
    component: ImagenConRecortar,
    supportedTypes: ["binary"],
});