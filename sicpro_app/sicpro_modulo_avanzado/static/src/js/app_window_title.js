/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

patch(WebClient.prototype, "sicpro_modulo_avanzado.WebClient", {
    setup() {
        this._super.apply(this, arguments);
        const app_system_name = 'SICPRO ERP';
        this.title.setParts({ zopenerp: app_system_name }); // Nombre del Sistema
    }
});