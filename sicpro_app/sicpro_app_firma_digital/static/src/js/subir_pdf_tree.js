odoo.define('sicpro_app_firma_digital.subir_pdf_tree', function (require) {
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

odoo.define('sicpro_app_firma_digital.subir_pdf_control_tree', function (require) {
"use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var ModelSubirPDF = require('sicpro_app_firma_digital.subir_pdf_tree');
    var viewRegistry = require('web.view_registry');

    var FirmaSubirPDFListController = ListController.extend(ModelSubirPDF, {
        buttons_template: 'template_subir_pdf_tree',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_subir_pdf_tree': '_onSubirPDF',
        }),
    });

    var FirmaSubirPDFList2View = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: FirmaSubirPDFListController,
        }),
    });

    viewRegistry.add('firma_subir_pdf_tree', FirmaSubirPDFList2View);
});

