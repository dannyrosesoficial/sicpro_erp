odoo.define('sicpro_app_nube_etecsa.nube_etecsa', function(require) {
    "use strict";

    var core = require('web.core');
    var mixins = require('web.mixins');
    var rpc = require('web.rpc');
    var Session = require('web.Session');
    var QWeb = core.qweb;
    var _t = core._t;
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');


    var NUBE_ETECSA = Widget.extend({
        template: 'NUBE_ETECSA',
        events: {
            "click a": "link_nube_etecsa",
        },
         link_nube_etecsa: function (ev) {
            ev.preventDefault();
            return this._rpc({
                model: 'sicpro.modulo.nube.etecsa',
                method: 'api_conexion_nube_etecsa',
                args: [[this.getSession().user_context]],
            }) .then(function (url) {
                window.open(url, '_blank',);
            });
        },
    });

    rpc.query({
        model: 'res.users',
        method: 'has_group',
        args: ['base.group_user']
    })
    .then(function(is_employee) {
        console.log(is_employee);
        if (is_employee) {
            SystrayMenu.Items.push(NUBE_ETECSA);
        }
    });
});
