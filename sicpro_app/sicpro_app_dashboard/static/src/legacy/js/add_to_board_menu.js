odoo.define('sicpro_app_dashboard.AddToBoardMenu', function (require) {
    "use strict";

    const Context = require('web.Context');
    const Domain = require('web.Domain');
    const FavoriteMenu = require('web.FavoriteMenu');
    const { sprintf } = require('web.utils');
    const { useAutofocus } = require('web.custom_hooks');

    const { Component, useState } = owl;


    class AddToBoardMenu extends Component {
        constructor() {
            super(...arguments);

            this.interactive = true;
            this.state = useState({
                name: this.env.action.name || "",
                open: false,
            });

            useAutofocus();
        }

        //---------------------------------------------------------------------
        // Privado
        //---------------------------------------------------------------------

        /**
         * @private
         */
        async addToBoard() {
            const searchQuery = this.env.searchModel.get('query');
            const context = new Context(this.env.action.context);
            context.add(searchQuery.context);
            context.add({
                group_by: searchQuery.groupBy,
                orderedBy: searchQuery.orderedBy,
            });
            if (searchQuery.timeRanges && searchQuery.timeRanges.hasOwnProperty('fieldName')) {
                context.add({
                    comparison: searchQuery.timeRanges,
                });
            }
            let controllerQueryParams;
            this.env.searchModel.trigger('get-controller-query-params', params => {
                controllerQueryParams = params || {};
            });
            controllerQueryParams.context = controllerQueryParams.context || {};
            const queryContext = controllerQueryParams.context;
            delete controllerQueryParams.context;
            context.add(Object.assign(controllerQueryParams, queryContext));

            const domainArray = new Domain(this.env.action.domain || []);
            const domain = Domain.prototype.normalizeArray(domainArray.toArray().concat(searchQuery.domain));

            const evalutatedContext = context.eval();
            for (const key in evalutatedContext) {
                if (evalutatedContext.hasOwnProperty(key) && /^search_default_/.test(key)) {
                    delete evalutatedContext[key];
                }
            }
            evalutatedContext.dashboard_merge_domains_contexts = false;

            Object.assign(this.state, {
                name: $(".o_input").val() || "",
                open: false,
            });

            const result = await this.rpc({
                route: '/sicpro_app_dashboard/add_to_dashboard',
                params: {
                    action_id: this.env.action.id || false,
                    context_to_save: evalutatedContext,
                    domain: domain,
                    view_mode: this.env.view.type,
                    name: this.state.name,
                },
            });
            if (result) {
                this.env.services.notification.notify({
                    title: sprintf(this.env._t("'%s' Agregado a su Dashboard"), this.state.name),
                    message: this.env._t("Por favor refresque el navegador para visualizar los cambios."),
                    type: 'warning',
                });
            } else {
                this.env.services.notification.notify({
                    message: this.env._t("No se ha agregado ningún filtro a su Dashboard"),
                    type: 'danger',
                });
            }
        }

        //---------------------------------------------------------------------
        // Manipuladores
        //---------------------------------------------------------------------

        /**
         * @private
         * @param {KeyboardEvent} ev
         */
        onInputKeydown(ev) {
            switch (ev.key) {
                case 'Enter':
                    ev.preventDefault();
                    this.addToBoard();
                    break;
                case 'Escape':
                    // Devuelve el foco al componente.
                    ev.preventDefault();
                    ev.target.blur();
                    break;
            }
        }

        //---------------------------------------------------------------------
        // Estático
        //---------------------------------------------------------------------

        /**
         * @param {Object} env
         * @returns {boolean}
         */
        static shouldBeDisplayed(env) {
            return env.action.type === 'ir.actions.act_window';
        }
    }

    AddToBoardMenu.props = {};
    AddToBoardMenu.template = 'sicpro_app_dashboard.AddToBoard';

    FavoriteMenu.registry.add('add-dashboard-menu', AddToBoardMenu, 10);

    return AddToBoardMenu;
});
