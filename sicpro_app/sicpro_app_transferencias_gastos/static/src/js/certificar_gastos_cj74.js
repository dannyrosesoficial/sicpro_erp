odoo.define('transferencias.gastos.economia.wizard', function (require) {
"use strict";

    var core = require('web.core');
    var _t = core._t;

    return {

        _onCertificar: function (event) {
            this.do_action({
                res_model: "sicpro.app.transferencias.gastos.economia.wizard",
                name: _t("Certificar Gastos SAP"),
                views: [[false, "form"]],
                type: "ir.actions.act_window",
                target: "new",
            });
        },

    };
});

odoo.define('sicpro_app_certificar_cj74', function (require) {
"use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var TransferirSubirCJ74 = require('transferencias.gastos.economia.wizard');
    var viewRegistry = require('web.view_registry');

    var CertificarListController = ListController.extend(TransferirSubirCJ74, {
        buttons_template: 'template_certificar_cj74',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_button_certificar_cj74': '_onCertificar',
        }),
    });

    var CertificarList2View = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: CertificarListController,
        }),
    });

    viewRegistry.add('certificar_gastos_cj74', CertificarList2View);
});

