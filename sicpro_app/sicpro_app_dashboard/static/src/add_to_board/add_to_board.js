/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useAutofocus, useService } from "@web/core/utils/hooks";
import { sprintf } from "@web/core/utils/strings";

const { Component, useState } = owl;
const favoriteMenuRegistry = registry.category("favoriteMenu");

/**
 * @extends Component
 */
export class AddToBoard extends Component {
    setup() {
        this.notification = useService("notification");
        this.rpc = useService("rpc");
        this.state = useState({ name: this.env.config.displayName });

        useAutofocus();
    }

    //---------------------------------------------------------------------
    // Protected
    //---------------------------------------------------------------------

    async addToBoard() {
        const { domain } = this.env.searchModel;
        const { context } = this.env.searchModel.getIrFilterValues();
        const contextToSave = {
            ...context,
            orderedBy: this.env.searchModel.orderBy,
            dashboard_merge_domains_contexts: false,
        };

        const result = await this.rpc("/sicpro_app_dashboard/add_to_dashboard", {
            action_id: this.env.config.actionId,
            context_to_save: contextToSave,
            domain,
            name: this.state.name,
            view_mode: this.env.config.viewType,
        });

        if (result) {
            this.notification.add(
                this.env._t("Por favor refresque el navegador para visualizar los cambios."),
                {
                    title: sprintf(this.env._t(`"%s" Agregado a su Dashboard`), this.state.name),
                    type: "warning",
                }
            );
            this.state.name = this.env.config.displayName;
        } else {
            this.notification.add(this.env._t("No se ha agregado ningún filtro a su Dashboard"), {
                type: "danger",
            });
        }
    }

    //---------------------------------------------------------------------
    // Handlers
    //---------------------------------------------------------------------

    /**
     * @param {KeyboardEvent} ev
     */
    onInputKeydown(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            this.addToBoard();
        }
    }
}

AddToBoard.template = "sicpro_app_dashboard.AddToBoard";

const addToBoardItem = {
    Component: AddToBoard,
    groupNumber: 4,
    isDisplayed: ({ config }) => config.actionType === "ir.actions.act_window",
};

favoriteMenuRegistry.add("add-to-dashboard", addToBoardItem, { sequence: 10 });
