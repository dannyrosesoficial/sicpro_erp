odoo.define('user_menu.data', function (require) {
"use strict";

var page=require('web.UserMenu');
var ajax = require('web.ajax');
var rpc = require('web.rpc');

var usepage=page.include({
   _onMenuCambio_Version: function () {
       var self = this;
       return self._rpc({
                    route: "/web/action/load",
                   params: {
                   action_id: "sicpro_app_administracion.menu_administracion_cambios_version_action",
                   },
               }).then(function (result) {
                    result.res_id = 1;
                    self.do_action(result);
               });
       },
   })
});

