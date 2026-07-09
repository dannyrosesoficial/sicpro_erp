/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        this.actionService = useService("action");
    },

    /**
     * Acción para Importar Datos
     * Corregido: Agregada coma al final y ajustada la acción de importación
     */
    _onImportarDatos() {
        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "import",
            params: {
                model: "sicpro.app.medios.informaticos.importar",
                context: this.props.context,
            },
        });
    }, // <-- Esta coma es obligatoria en la definición del objeto del patch

    /**
     * Acción para Actualizar (Wizard)
     */
    onActualizarDatos() {
        this.actionService.doAction({
            res_model: "sicpro.app.medios.informaticos.importar.wizard",
            name: _t("Actualizar inventario"),
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            target: "new",
        });
    },
});