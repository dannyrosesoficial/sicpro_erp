/** @odoo-module **/

import {UserMenu} from "@web/webclient/user_menu/user_menu";
import {patch} from "@web/core/utils/patch";
import {browser} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";
import {session} from "@web/session";

var rpc = require("web.rpc");

const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, "sicpro_modulo_avanzado.UserMenu", {
    setup() {
        this._super.apply(this, arguments);
        userMenuRegistry.remove("documentation");
        userMenuRegistry.remove("support");
        userMenuRegistry.remove("odoo_account");

        // Menu Perfil 1
        const app_menu_perfil_1 = session.app_menu_perfil_1;
        if (app_menu_perfil_1 === 'True') {
            userMenuRegistry.add("menu_perfil_1", menu_perfil_1);
        }

        // Menu Perfil 2
        const app_menu_perfil_2 = session.app_menu_perfil_2;
        if (app_menu_perfil_2 === 'True') {
            userMenuRegistry.add("menu_perfil_2", menu_perfil_2);
        }

        // Menu Perfil 3
        const app_menu_perfil_3 = session.app_menu_perfil_3;
        if (app_menu_perfil_3 === 'True') {
            userMenuRegistry.add("menu_perfil_3", menu_perfil_3);
        }

        // Menu Perfil 4
        const app_menu_perfil_4 = session.app_menu_perfil_4;
        if (app_menu_perfil_4 === 'True') {
            userMenuRegistry.add("menu_perfil_4", menu_perfil_4);
        }

        // Menu Perfil 5
        const app_menu_perfil_5 = session.app_menu_perfil_5;
        if (app_menu_perfil_5 === 'True') {
            userMenuRegistry.add("menu_perfil_5", menu_perfil_5);
        }

        // Menu Perfil 6
        const app_menu_perfil_6 = session.app_menu_perfil_6;
        if (app_menu_perfil_6 === 'True') {
            userMenuRegistry.add("menu_perfil_6", menu_perfil_6);
        }

        // Menu Separador 0
        userMenuRegistry.add("separador0", separador0);

        // Menu Separador 1
        const app_menu_separador_1 = session.app_menu_separador_1;
        if (app_menu_separador_1 === 'True') {
            userMenuRegistry.add("separador1", separador1);
        }

        // Menu Separador 2
        const app_menu_separador_2 = session.app_menu_separador_2;
        if (app_menu_separador_2 === 'True') {
            userMenuRegistry.add("separador2", separador2);
        }

        // Menu Separador 3
        const app_menu_separador_3 = session.app_menu_separador_3;
        if (app_menu_separador_3 === 'True') {
            userMenuRegistry.add("separador3", separador3);
        }

        // Menu Separador 4
        const app_menu_separador_4 = session.app_menu_separador_4;
        if (app_menu_separador_4 === 'True') {
            userMenuRegistry.add("separador4", separador4);
        }

    },
});

function menu_perfil_1(env) {
    const titulo = session.app_menu_perfil_1_titulo;
    const url = session.app_menu_perfil_1_url;
    const secuencia = session.app_menu_perfil_1_sequence;
    return {
        type: "item",
        id: "menu_perfil_1",
        description: env._t(titulo),
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: secuencia,
    };
}

function menu_perfil_2(env) {
    const titulo = session.app_menu_perfil_2_titulo;
    const url = session.app_menu_perfil_2_url;
    const secuencia = session.app_menu_perfil_2_sequence;
    return {
        type: "item",
        id: "menu_perfil_2",
        description: env._t(titulo),
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: secuencia,
    };
}

function menu_perfil_3(env) {
    const titulo = session.app_menu_perfil_3_titulo;
    const url = session.app_menu_perfil_3_url;
    const secuencia = session.app_menu_perfil_3_sequence;
    return {
        type: "item",
        id: "menu_perfil_3",
        description: env._t(titulo),
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: secuencia,
    };
}

function menu_perfil_4(env) {
    const titulo = session.app_menu_perfil_4_titulo;
    const url = session.app_menu_perfil_4_url;
    const secuencia = session.app_menu_perfil_4_sequence;
    return {
        type: "item",
        id: "menu_perfil_4",
        description: env._t(titulo),
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: secuencia,
    };
}

function menu_perfil_5(env) {
    const titulo = session.app_menu_perfil_5_titulo;
    const url = session.app_menu_perfil_5_url;
    const secuencia = session.app_menu_perfil_5_sequence;
    return {
        type: "item",
        id: "menu_perfil_5",
        description: env._t(titulo),
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: secuencia,
    };
}

function menu_perfil_6(env) {
    const titulo = session.app_menu_perfil_6_titulo;
    const url = session.app_menu_perfil_6_url;
    const secuencia = session.app_menu_perfil_6_sequence;
    return {
        type: "item",
        id: "menu_perfil_6",
        description: env._t(titulo),
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: secuencia,
    };
}

function separador0() {
    return {
        type: "separator",
        sequence: 25,
    };
}

function separador1(env) {
    const secuencia = session.app_menu_separador_1_sequence;
    return {
        type: "separator",
        sequence: secuencia,
    };
}

function separador2(env) {
    const secuencia = session.app_menu_separador_2_sequence;
    return {
        type: "separator",
        sequence: secuencia,
    };
}

function separador3(env) {
    const secuencia = session.app_menu_separador_3_sequence;
    return {
        type: "separator",
        sequence: secuencia,
    };
}

function separador4(env) {
    const secuencia = session.app_menu_separador_4_sequence;
    return {
        type: "separator",
        sequence: secuencia,
    };
}