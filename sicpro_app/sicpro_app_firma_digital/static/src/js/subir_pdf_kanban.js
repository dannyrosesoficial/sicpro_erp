odoo.define('sicpro_app_firma_digital.subir_pdf_kanban', function (require) {
"use strict";

    var core = require('web.core');
    var _t = core._t;

    return {
        _onSubirPDF: function (event) {
            this.do_action({
                res_model: "sicpro.app.firma.subir.pdf.wizard",
                name: _t("Subir nuevo documento"),
                views: [[false, "form"]],
                type: "ir.actions.act_window",
                target: "new",
            });
        },
    };
});

odoo.define('sicpro_app_firma_digital.subir_pdf_control_kanban', function (require) {
"use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var ModelSubirPDF = require('sicpro_app_firma_digital.subir_pdf_kanban');
    var viewRegistry = require('web.view_registry');
    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');

    var FirmaSubirPDFKanbanController = KanbanController.extend(ModelSubirPDF, {
        buttons_template: 'template_subir_pdf_kanban',
        events: _.extend({}, KanbanController.prototype.events, {
            'click .o_subir_pdf_kanban': '_onSubirPDF',
        }),
    });


    var FirmaSubirPDFKanban2View = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: FirmaSubirPDFKanbanController,
        }),
    });


    viewRegistry.add('firma_subir_pdf_kanban', FirmaSubirPDFKanban2View);
});
