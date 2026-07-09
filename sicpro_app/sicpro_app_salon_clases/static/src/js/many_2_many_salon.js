odoo.define('sicpro_app_salon_clases.many_2_Many_BinarySalon', function (require) {
    "use strict";

    // Importando las Cosas para crear el widget
    var base_rf = require('web.relational_fields');
    var AbstractField = require('web.AbstractField');
    var many2ManyBinary = base_rf.FieldMany2ManyBinaryMultiFiles;
    var fieldRegistry = require('web.field_registry');

    var many2ManyBinarySalon = many2ManyBinary.extend({
        template: "FieldBinaryFileUploaderSalon",
        template_files: "FieldBinaryFileUploaderSalon.files",


        init: function () {
            AbstractField.prototype.init.apply(this, arguments);

            if (this.field.type !== 'many2many') {
                var msg = _t("The type of the field '%s' must be a many2many field.");
                throw _.str.sprintf(msg, this.field.string);
            }

            this.uploadedFiles = {};
            this.uploadingFiles = [];
            this.fileupload_id = _.uniqueId('oe_fileupload_temp');
            this.accepted_file_extensions = (this.nodeOptions && this.nodeOptions.accepted_file_extensions) || this.accepted_file_extensions || '*';
            $(window).on(this.fileupload_id, this._onFileLoaded.bind(this));

            this.metadata = {};
        },

        _getFileUrl: function (attachment) {
            return '/salon_clases/content/' + attachment.id + '?download=true';
        },

        _onDelete: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();

            var fileID = $(ev.currentTarget).data('id');
            var record = _.findWhere(this.value.data, {res_id: fileID});
            if (record) {
                this._setValue({
                    operation: 'FORGET',
                    ids: [record.id],
                });
                var metadata = this.metadata[record.id];
                if (!metadata || metadata.allowUnlink) {
                    this._rpc({
                        model: 'sicpro.app.salon.clases.adjuntos',
                        method: 'unlink',
                        args: [record.res_id],
                    });
                }
            }
        },

        _onFileChanged: function (ev) {
            var self = this;
            ev.stopPropagation();

            var files = ev.target.files;
            var attachment_ids = this.value.res_ids;

        // Don't create an attachment if the upload window is cancelled.
        if(files.length === 0)
            return;

        _.each(files, function (file) {
            var record = _.find(self.value.data, function (attachment) {
                return attachment.data.name === file.name;
            });
            if (record) {
                var metadata = self.metadata[record.id];
                if (!metadata || metadata.allowUnlink) {
                    // there is a existing attachment with the same name so we
                    // replace it
                    attachment_ids = _.without(attachment_ids, record.res_id);
                    self._rpc({
                        model: 'sicpro.app.salon.clases.adjuntos',
                        method: 'unlink',
                        args: [record.res_id],
                    });
                }
            }
            self.uploadingFiles.push(file);
        });

        this._setValue({
            operation: 'REPLACE_WITH',
            ids: attachment_ids,
        });

        this.$('form.o_form_binary_form').submit();
        this.$('.oe_fileupload').hide();
        ev.target.value = "";
    },

});

    fieldRegistry.add('many_2_Many_BinarySalon', many2ManyBinarySalon);

    return many2ManyBinarySalon;

});
