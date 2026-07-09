odoo.define('viveres.distribuir.productos', function (require) {
    "use strict";
    
        var core = require('web.core');
        var _t = core._t;
    
        return {
    
            _onDistribuir: function (event) {
                this.do_action({
                    res_model: "sicpro.app.viveres.trabajadores.entrega.wizard",
                    name: _t("Distribuir productos"),
                    views: [[false, "form"]],
                    type: "ir.actions.act_window",
                    target: "new",
                });
            },
        };
    });
    
    odoo.define('sicpro_app_distribuir_productos', function (require) {
    "use strict";
    
        var core = require('web.core');
        var ListController = require('web.ListController');
        var ListView = require('web.ListView');
        var DistribuirProductos = require('viveres.distribuir.productos');
        var viewRegistry = require('web.view_registry');
    
        var DistribuirListController = ListController.extend(DistribuirProductos, {
            buttons_template: 'template_viveres_distribuir_productos',
            events: _.extend({}, ListController.prototype.events, {
                'click .o_button_distribuir_productos': '_onDistribuir',
            }),
        });
    
        var DistribuirList2View = ListView.extend({
            config: _.extend({}, ListView.prototype.config, {
                Controller: DistribuirListController,
            }),
        });
    
        viewRegistry.add('distribuir_productos', DistribuirList2View);
    });
    