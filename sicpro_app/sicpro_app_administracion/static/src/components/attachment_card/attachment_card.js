/** @odoo-module */

import { AttachmentCard } from '@mail/components/attachment_card/attachment_card';
import { patch } from 'web.utils';
import core from 'web.core';
const _t = core._t;

patch(AttachmentCard.prototype, 'sicpro_app_administracion/static/src/components/attachment_card/attachment_card.js', {
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * @override
     */
    _onClickComment(ev) {
        ev.preventDefault();
        var attachment_id = ev.target.dataset.id;
        this.trigger('o-update-attachment-description', {
            res_id: parseInt(attachment_id),
            onSaved: (record, changed) => {
                if (changed) {
                    this.trigger('reload', { keepChanges: true });
                }
            },
        });
    },

});
