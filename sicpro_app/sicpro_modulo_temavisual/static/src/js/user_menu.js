/** @odoo-module **/

import {UserMenu} from "@web/webclient/user_menu/user_menu";
import {patch} from "@web/core/utils/patch";
import {registry} from "@web/core/registry";

const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, "sicpro_modulo_temavisual.UserMenu", {
    setup() {
        this._super.apply(this, arguments);
        userMenuRegistry

        userMenuRegistry.add("separator30", separator30)
        userMenuRegistry.add("modo_claro_oscuro", modo_claro_oscuro)
        userMenuRegistry.add("modo_barra_lateral", modo_barra_lateral)
        /// userMenuRegistry.add("separator32", separator32)
    },

});

function separator30() {
    return {
        type: "separator",
        sequence: 30,
    };
}

function modo_claro_oscuro(env) {
    let titulo;
    if (localStorage.darkMode !== 'false') {
        titulo = 'Modo Claro ○';
    } else {
        titulo = 'Modo Oscuro ●';
    }
    return {
        type: "item",
        id: "modo_claro_oscuro",
        description: env._t(titulo),
        callback: () => {
            $('.oh_dashboards').removeClass('observed');
            let valor = true;
            if (localStorage.darkMode !== 'false') {
                valor = false;
            }
            localStorage.setItem("darkMode", valor);
            document.documentElement.toggleAttribute("dark-mode");
        },
        sequence: 31,
    };
}

function modo_barra_lateral(env) {
    let titulo_barra;
    if (localStorage.barra_lateral !== 'false') {
        titulo_barra = 'Ocultar Barra Lateral';
    } else {
        titulo_barra = 'Visualizar Barra Lateral';
    }
    return {
        type: "item",
        id: "modo_barra_lateral",
        description: env._t(titulo_barra),
        callback: () => {
            let valor = true;
            if (localStorage.barra_lateral !== 'false') {
                valor = false;
            }
            localStorage.setItem("barra_lateral", valor);
        },
        sequence: 31,
    };
}

function separator32() {
    return {
        type: "separator",
        sequence: 32,
    };
}

