odoo.define('medios.informaticos.importar', function (require) {
    "use strict";
    
        var core = require('web.core');
        var _t = core._t;
    
        return {
    
            _onSubir: function (event) {
                this.do_action({
                    type: "ir.actions.act_url",
                    target: "self",
                    url: "/web#model=sicpro.app.medios.informaticos.importar&action=import",
                });
            },
    
            _onActualizar: function (event) {
                this.do_action({
                    res_model: "sicpro.app.medios.informaticos.importar.wizard",
                    name: _t("Actualizar inventario"),
                    views: [[false, "form"]],
                    type: "ir.actions.act_window",
                    target: "new",
                });
            },
        };
    });
    
    odoo.define('sicpro_app_importar_datos', function (require) {
    "use strict";
    
        var core = require('web.core');
        var ListController = require('web.ListController');
        var ListView = require('web.ListView');
        var ImportarDatos = require('medios.informaticos.importar');
        var viewRegistry = require('web.view_registry');
    
        var ImportarListController = ListController.extend(ImportarDatos, {
            buttons_template: 'template_importar_medios_informaticos',
            events: _.extend({}, ListController.prototype.events, {
                'click .o_button_importar_datos': '_onSubir',
                'click .o_button_actualizar_datos': '_onActualizar',
            }),
        });
    
        var ImportarList2View = ListView.extend({
            config: _.extend({}, ListView.prototype.config, {
                Controller: ImportarListController,
            }),
        });
    
        viewRegistry.add('importar_datos', ImportarList2View);
    });
    