/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class DistribuirListController extends ListController {
    setup() {
        super.setup();
        this.actionService = useService("action");
    }

    /**
     * Acción para Distribuir productos (Wizard)
     * Sustituye al antiguo _onDistribuir
     */
    onDistribuir() {
        this.actionService.doAction({
            res_model: "sicpro.app.viveres.trabajadores.entrega.wizard",
            name: _t("Distribuir productos"),
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            target: "new",
        });
    }
}

// Registramos la vista personalizada con el js_class 'distribuir_productos'
registry.category("views").add("distribuir_productos", {
    ...listView,
    Controller: DistribuirListController,
    buttonTemplate: "sicpro_app_viveres.template_viveres_distribuir_productos",
});