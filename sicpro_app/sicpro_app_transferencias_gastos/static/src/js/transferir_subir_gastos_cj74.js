odoo.define('transferencias.gastos.cj74.wizard', function (require) {
"use strict";

    var core = require('web.core');
    var _t = core._t;

    return {

        _onTransferir: function (event) {
            this.do_action({
                res_model: "sicpro.app.transferencias.gastos.cj74.wizard",
                name: _t("Transferir CJ74 SAP"),
                views: [[false, "form"]],
                type: "ir.actions.act_window",
                target: "new",
            });
        },

        _onSubir: function (event) {
            this.do_action({
                type: "ir.actions.act_url",
                target: "self",
                url: "/web#model=sicpro.app.transferencias.gastos.importar&action=import",
            });
        },


    };
});

odoo.define('sicpro_app_transferir_cj74', function (require) {
"use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var TransferirSubirCJ74 = require('transferencias.gastos.cj74.wizard');
    var viewRegistry = require('web.view_registry');

    var TransferirSubirListController = ListController.extend(TransferirSubirCJ74, {
        buttons_template: 'template_transferir_cj74',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_button_transferir_cj74': '_onTransferir',
            'click .o_button_subir_cj74': '_onSubir',
        }),
    });

    var TransferirSubirList2View = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TransferirSubirListController,
        }),
    });

    viewRegistry.add('transferir_subir_cj74', TransferirSubirList2View);
});

