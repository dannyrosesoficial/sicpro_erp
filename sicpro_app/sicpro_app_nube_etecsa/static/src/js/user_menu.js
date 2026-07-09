/** @odoo-module **/

import {registry} from "@web/core/registry";


const userMenuRegistry = registry.category("user_menuitems");

function menu_nube_etecsa() {
    userMenuRegistry.add("nube_etecsa", function ajustesItem(env) {
        return {
            type: "item",
            id: "nube_etecsa",
            description: env._t("Nextcloud Nube Etecsa"),
            callback: () => {
                env.services.action.doAction({
                    name: env._t("Nextcloud Nube Etecsa"),
                    target: "new",
                    type: "ir.actions.act_url",
                    url: "https://nube.etecsa.cu/",
                });
            },
            sequence: 60,
        };
    });
}

menu_nube_etecsa();

