odoo.define('sicpro_app_contratos.ActionManager', function (require) {
"use strict";


var ActionManager = require('web.ActionManager');

ActionManager.include({
    //--------------------------------------------------------------------------
    // Privado
    //--------------------------------------------------------------------------

     // CAMBIAR EL MODELO DE DATOS
    _executeWindowAction: function (action) {
        if (action.res_model === 'sicpro.app.contratos.dashboard' && action.view_mode === 'form') {
            action.target = 'inline';
            _.extend(action.flags, {
                hasActionMenus: false,
                hasSearchView: false,
                headless: true,
            });
        }
        return this._super.apply(this, arguments);
    },
});

});
