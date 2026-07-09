
odoo.define('sicpro_modulo_web_login.actions', function (require) {
"use strict";

   var basic_fields = require('web.basic_fields');
   var registry = require('web.field_registry');

   var no_copy_paste = basic_fields.FieldText.extend({

        events: _.extend({}, basic_fields.FieldText.prototype.events, {
            'copy': '_onCopyPaste',
            'paste': '_onCopyPaste',
        }),

        _onCopyPaste: function(ev) {
            ev.preventDefault();
            alert("Copy/Paste Disabled!");
        },
   });

   registry.add('no_copy_paste', no_copy_paste);
});
