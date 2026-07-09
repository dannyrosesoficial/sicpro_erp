odoo.define('sicpro_app_trabajadores/static/src/models/messaging/messaging.js', function (require) {
'use strict';

const {
    registerInstancePatchModel,
} = require('mail/static/src/model/model_core.js');

registerInstancePatchModel('mail.messaging', 'sicpro_app_trabajadores/static/src/models/messaging/messaging.js', {
    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     * @param {integer} [param0.employeeId]
     */
    async getChat({ employeeId }) {
        if (employeeId) {
            const employee = this.env.models['sicpro.app.trabajadores'].insert({ id: employeeId });
            return employee.getChat();
        }
        return this._super(...arguments);
    },
    /**
     * @override
     */
    async openProfile({ id, model }) {
        if (model === 'sicpro.app.trabajadores' || model === 'sicpro.app.trabajadores') {
            const employee = this.env.models['sicpro.app.trabajadores'].insert({ id });
            return employee.openProfile();
        }
        return this._super(...arguments);
    },
});

});
