odoo.define('trabajadores.generar.cierre', function (require) {
    "use strict";
    
        var core = require('web.core');
        var _t = core._t;
    
        return {
    
            _onGenerar: function (event) {
                this.do_action({
                    res_model: "sicpro.app.trabajadores.cierre.wizard",
                    name: _t("Generar cierre"),
                    views: [[false, "form"]],
                    type: "ir.actions.act_window",
                    target: "new",
                });
            },
        };
    });
    
odoo.define('sicpro_app_generar_cierre', function (require) {
    "use strict";
    
        var core = require('web.core');
        var ListController = require('web.ListController');
        var ListView = require('web.ListView');
        var CargarDatos = require('trabajadores.generar.cierre');
        var viewRegistry = require('web.view_registry');
    
        var GenerarListController = ListController.extend(CargarDatos, {
            buttons_template: 'template_cierre_trabajadores',
            events: _.extend({}, ListController.prototype.events, {
                'click .o_button_generar_cierre': '_onGenerar',
            }),
        });
    
        var GenerarList2View = ListView.extend({
            config: _.extend({}, ListView.prototype.config, {
                Controller: GenerarListController,
            }),
        });
    
        viewRegistry.add('generar_cierre', GenerarList2View);
    });
    