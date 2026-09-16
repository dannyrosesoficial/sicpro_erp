/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { onWillStart } from "@odoo/owl";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);

        // REGLA: El setup NO debe ser async en Odoo 19 para evitar errores de ciclo de vida.
        onWillStart(async () => {
            // Detectar si es wizard
            this.isSicproWizard = !!(this.env.dialogData || this.props.actionType === "ir.actions.act_window");

            // Lógica original: si tiene resId y viene en edit, forzamos readonly
            if (!this.isSicproWizard && this.props.resId && this.model.config.mode === "edit") {
                this.model.config.mode = "readonly";
            }
        });
    },

    isReadOnly() {
        // Si no hay modelo o es wizard, no mostramos nuestro botón
        if (!this.model || this.isSicproWizard) return false;
        return this.model.config.mode === "readonly";
    },

    async onClickEditBtn() {
        // --- CÓDIGO ORIGINAL (COMENTADO SEGÚN REGLA) ---
        /*
        const record = this.model.root;
        await record.switchMode("edit");
        record.dirty = true;
        */

        const record = this.model.root;
        if (record) {
            await record.switchMode("edit");
            // Sincronizamos el config para que el t-if del XML reaccione
            this.model.config.mode = "edit";
            record.dirty = true;
        }
    },

    async save(params) {
        // Usamos la lógica de tu original pero simplificada para Odoo 19
        const saved = await super.save(...arguments);

        if (saved && !this.isSicproWizard) {
            await this.model.root.switchMode("readonly", false);
            this.model.config.mode = "readonly";
        }
        return saved;
    },

    async discard() {
        await super.discard(...arguments);
        if (!this.isSicproWizard) {
            await this.model.root.switchMode("readonly");
            this.model.config.mode = "readonly";
        }
    },
});