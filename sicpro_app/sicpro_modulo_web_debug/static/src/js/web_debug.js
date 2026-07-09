/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";
import { user } from "@web/core/user";

export class WebDebug extends Component {
    static template = "sicpro_modulo_web_debug.WKDebug";
    setup(){
        this.orm = useService("orm");
        onWillStart(async () => {
            this.is_employee = await this.orm.call("res.users", "has_group", [user.userId],{group_ext_id: 'base.group_system'})
            .then(function (is_employee){
                return is_employee;
            });  
          });
             
    }

    oe_activate_debug_mode(ev) {
        ev.preventDefault();
        var final = window.location.href.split('#')[1]
        let params = new URLSearchParams(window.location.search);
        params.set('debug', '1');
        var loc = window.location.pathname + '?' + params.toString() + '#' + final;
        window.location=loc;
        console.log(loc);

    }
 
}


export const systrayDebug = {
    Component:WebDebug,
};

registry
    .category("systray")
    .add("sicpro_modulo_web_debug.WKDebug", systrayDebug, { sequence: 10 });
