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
        events: { "click .oe_link_nube_etecsa": "oe_link_nube_etecsa",},

        oe_link_nube_etecsa: function(event) {
            event.preventDefault();
            window.open('https://nube.etecsa.cu/', '_blank',);
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
