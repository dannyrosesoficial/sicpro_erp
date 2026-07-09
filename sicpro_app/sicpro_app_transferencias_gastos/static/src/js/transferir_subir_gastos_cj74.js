/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        // Inyectamos el servicio de acciones una sola vez
        this.actionService = useService("action");
    },

    /**
     * Abre el Wizard de Transferencia
     */
    _onTransferir_cj74() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "sicpro.app.transferencias.gastos.cj74.wizard",
            name: _t("Transferir CJ74 SAP"),
            views: [[false, "form"]],
            target: "new",
            context: this.props.context,
        });
    },

    /**
     * Abre la interfaz nativa de importación
     */
    _onSubir_cj74() {
        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "import",
            params: {
                model: "sicpro.app.transferencias.gastos.importar",
                context: this.props.context,
            },
        });
    }
});