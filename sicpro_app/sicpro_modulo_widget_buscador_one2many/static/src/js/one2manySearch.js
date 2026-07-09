/** @odoo-module **/

import { registry } from "@web/core/registry";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { useRef } from "@odoo/owl";

export class One2ManySearch extends X2ManyField {
    static template = "sicpro_modulo_widget_buscador_one2many.One2ManySearch";

    setup() {
        super.setup();
        this.searchField = useRef("searchField");
    }

    /**
     * Filtra dinámicamente las filas de la tabla sin llamar al servidor
     */
    _onSearchInput(ev) {
        const value = ev.target.value.toLowerCase();
        // Buscamos la tabla dentro del componente actual
        const rows = this.root.el.querySelectorAll(".o_list_table tr:not(.o_column_sortable)");

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            // Si el texto coincide, mostramos la fila, si no, aplicamos d-none (Bootstrap 5)
            if (text.includes(value)) {
                row.classList.remove("d-none");
            } else {
                row.classList.add("d-none");
            }
        });
    }
}

// Registramos el nuevo componente como un widget disponible para el XML
registry.category("fields").add("one2many_search", {
    ...x2ManyField,
    component: One2ManySearch,
});