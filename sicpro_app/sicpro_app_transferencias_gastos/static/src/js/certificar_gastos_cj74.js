/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        this.actionService = useService("action");
    },
    _onCertificar_cj74() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "sicpro.app.transferencias.gastos.economia.wizard",
            name: "Certificar Gastos SAP",
            views: [[false, "form"]],
            target: "new",
        });
    }
});