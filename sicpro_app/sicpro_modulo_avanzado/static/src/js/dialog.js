/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

patch(Dialog.prototype, "sicpro_modulo_avanzado.Dialog", {
    setup() {
        this._super.apply(this, arguments);
        const app_system_name = "SICPRO ERP";
        this.title = app_system_name;
    },

});

