odoo.define('sicpro_app_contratos.bank_statement', function(require) {
    "use strict";

    var KanbanController = require("web.KanbanController");
    var ListController = require("web.ListController");

    var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (this.modelName === "sicpro.app.contratos.banco") {
                var data = this.model.get(this.handle);
                if (data.context.journal_type !== 'cash') {
                    this.$buttons.find('button.o_button_import').hide();
                }
            }
        }
    };

    KanbanController.include(includeDict);
    ListController.include(includeDict);
});