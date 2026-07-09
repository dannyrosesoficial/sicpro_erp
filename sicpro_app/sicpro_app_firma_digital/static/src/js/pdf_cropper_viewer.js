odoo.define('sicpro_app_firma_digital.pdf_viewer2', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var framework = require('web.framework');
var session = require('web.session');
var utils = require('web.utils');
const { hidePDFJSButtons } = require('@web/legacy/js/libs/pdfjs');
var Registry = require('web.field_registry');

require("web.zoomodoo");

var qweb = core.qweb;
var _t = core._t;
var _lt = core._lt;



var AbstractFieldBinary = AbstractField.extend({
    events: _.extend({}, AbstractField.prototype.events, {
        'change .o_input_file': 'on_file_change',
        'click .o_select_file_button': function () {
            this.$('.o_input_file').click();
        },
        'click .o_clear_file_button': '_onClearClick',
    }),
    init: function (parent, name, record) {
        this._super.apply(this, arguments);
        this.fields = record.fields;
        this.useFileAPI = !!window.FileReader;
        this.max_upload_size = session.max_file_upload_size || 128 * 1024 * 1024;
        this.accepted_file_extensions = (this.nodeOptions && this.nodeOptions.accepted_file_extensions) || this.accepted_file_extensions || '*';
        if (!this.useFileAPI) {
            var self = this;
            this.fileupload_id = _.uniqueId('o_fileupload');
            $(window).on(this.fileupload_id, function () {
                var args = [].slice.call(arguments).slice(1);
                self.on_file_uploaded.apply(self, args);
            });
        }
    },
    destroy: function () {
        if (this.fileupload_id) {
            $(window).off(this.fileupload_id);
        }
        this._super.apply(this, arguments);
    },
    on_file_change: function (e) {
        var self = this;
        var file_node = e.target;
        if ((this.useFileAPI && file_node.files.length) || (!this.useFileAPI && $(file_node).val() !== '')) {
            if (this.useFileAPI) {
                var file = file_node.files[0];
                if (file.size > this.max_upload_size) {
                    var msg = _t("The selected file exceed the maximum file size of %s.");
                    this.displayNotification({ title: _t("File upload"), message: _.str.sprintf(msg, utils.human_size(this.max_upload_size)), type: 'danger' });
                    return false;
                }
                utils.getDataURLFromFile(file).then(function (data) {
                    data = data.split(',')[1];
                    self.on_file_uploaded(file.size, file.name, file.type, data);
                });
            } else {
                this.$('form.o_form_binary_form').submit();
            }
            this.$('.o_form_binary_progress').show();
            this.$('button').hide();
        }
    },
    on_file_uploaded: function (size, name) {
        if (size === false) {
            this.displayNotification({ message: _t("There was a problem while uploading your file"), type: 'danger' });
            console.warn("Error while uploading file : ", name);
        } else {
            this.on_file_uploaded_and_valid.apply(this, arguments);
        }
        this.$('.o_form_binary_progress').hide();
        this.$('button').show();
    },
    on_file_uploaded_and_valid: function (size, name, content_type, file_base64) {
        this.set_filename(name);
        this._setValue(file_base64);
        this._render();
    },
    /**
     * We need to update another field.  This method is so deprecated it is not
     * even funny.  We need to replace this with the mechanism of field widgets
     * declaring statically that they need to listen to every changes in other
     * fields
     *
     * @deprecated
     *
     * @param {any} value
     */
    set_filename: function (value) {
        var filename = this.attrs.filename;
        if (filename && filename in this.fields) {
            var changes = {};
            changes[filename] = value;
            this.trigger_up('field_changed', {
                dataPointID: this.dataPointID,
                changes: changes,
                viewType: this.viewType,
            });
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
    /**
     * Clear the file input
     *
     * @private
     */
    _clearFile: function (){
        var self = this;
        this.$('.o_input_file').val('');
        this.set_filename('');
        if (!this.isDestroyed()) {
            this._setValue(false).then(function() {
                self._render();
            });
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * On "clear file" button click
     *
     * @param {MouseEvent} ev
     * @private
     */
    _onClearClick: function (ev) {
        this._clearFile();
    },
});

var FieldBinaryFile = AbstractFieldBinary.extend({
    description: _lt("File"),
    template: 'FieldBinaryFile',
    events: _.extend({}, AbstractFieldBinary.prototype.events, {
        'click': function (event) {
            if (this.mode === 'readonly' && this.value && this.recordData.id) {
                this.on_save_as(event);
            }
        },
        'click .o_input': function () { // eq[0]
            this.$('.o_input_file').click();
        },
    }),
    supportedFieldTypes: ['binary'],
    init: function () {
        this._super.apply(this, arguments);
        this.filename_value = this.recordData[this.attrs.filename];
    },
    _renderReadonly: function () {
        var visible = !!(this.value && this.res_id);
        this.$el.empty().css('cursor', 'not-allowed');
        this.do_toggle(visible);
        if (visible) {
            this.$el.css('cursor', 'pointer')
                    .text(this.filename_value || '')
                    .prepend($('<span class="fa fa-download"/>'), ' ');
        }
    },
    _renderEdit: function () {
        if (this.value) {
            this.$el.children().removeClass('o_hidden');
            this.$('.o_select_file_button').first().addClass('o_hidden');
            this.$('.o_input').eq(0).val(this.filename_value || this.value);
        } else {
            this.$el.children().addClass('o_hidden');
            this.$('.o_select_file_button').first().removeClass('o_hidden');
        }
    },
    set_filename: function (value) {
        this._super.apply(this, arguments);
        this.filename_value = value; // will be used in the re-render
        // the filename being edited but not yet saved, if the user clicks on
        // download, he'll get the file corresponding to the current value
        // stored in db, which isn't the one whose filename is displayed in the
        // input, so we disable the download button
        this.$('.o_save_file_button').prop('disabled', true);
    },
    on_save_as: function (ev) {
        if (!this.value) {
            this.displayNotification({ message: _t("The field is empty, there's nothing to save."), type: 'danger' });
            ev.stopPropagation();
        } else if (this.res_id) {
            framework.blockUI();
            var filename_fieldname = this.attrs.filename;
            this.getSession().get_file({
                complete: framework.unblockUI,
                data: {
                    'model': this.model,
                    'id': this.res_id,
                    'field': this.name,
                    'filename_field': filename_fieldname,
                    'filename': this.recordData[filename_fieldname] || "",
                    'download': true,
                    'data': utils.is_bin_size(this.value) ? null : this.value,
                },
                error: (error) => this.call('crash_manager', 'rpc_error', error),
                url: '/web/content',
            });
            ev.stopPropagation();
        }
    },
});

var FieldPdfCropperViewer = FieldBinaryFile.extend({
    description: _lt("PDF Viewer"),
    supportedFieldTypes: ['binary'],
    template: 'FieldPdfCropperViewer',
    accepted_file_extensions: 'application/pdf',
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.PDFViewerApplication = false;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {string} [fileURI] file URI if specified
     * @returns {string} the pdf viewer URI
     */
    _getURI: function (fileURI) {
        var page = this.recordData[this.name + '_page'] || 1;
        if (!fileURI) {
            var queryObj = {
                model: this.model,
                field: this.name,
                id: this.res_id,
            };
            var queryString = $.param(queryObj);
            fileURI = '/web/content?' + queryString;
        }
        fileURI = encodeURIComponent(fileURI);
        var viewerURL = '/web/static/lib/pdfjs/web/viewer.html?file=';
        return viewerURL + fileURI + '#page=' + page + '&zoom=165';
    },
    /**
     * @private
     * @override
     */
    _render: function () {
        var self = this;
        var $pdfViewer = this.$('.o_form_pdf_controls').children().add(this.$('.o_pdfview_iframe'));
        var $selectUpload = this.$('.o_select_file_button').first();
        var $iFrame = this.$('.o_pdf_cropper_view_iframe');

        $iFrame.on('load', function () {
            self.PDFViewerApplication = this.contentWindow.window.PDFViewerApplication;
        });
        if (this.mode === "readonly" && this.value) {
            $iFrame.attr('src', this._getURI());
        } else {
            if (this.value) {
                var binSize = utils.is_bin_size(this.value);
                $pdfViewer.removeClass('o_hidden');
                $selectUpload.addClass('o_hidden');
                if (binSize) {
                    $iFrame.attr('src', this._getURI());
                }
            } else {
                $pdfViewer.addClass('o_hidden');
                $selectUpload.removeClass('o_hidden');
            }
        }
        hidePDFJSButtons($iFrame[0]);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     * @param {Event} ev
     */
    on_file_change: function (ev) {
        this._super.apply(this, arguments);
        var files = ev.target.files;
        if (!files || files.length === 0) {
            return;
        }
        // TOCheck: is there requirement to fallback on FileReader if browser don't support URL
        var fileURI = URL.createObjectURL(files[0]);
        if (this.PDFViewerApplication) {
            this.PDFViewerApplication.open(fileURI, 0);
        } else {
            this.$('.o_pdf_cropper_view_iframe').attr('src', this._getURI(fileURI));
        }
    },
    /**
     * Remove the behaviour of on_save_as in FieldBinaryFile.
     *
     * @override
     * @private
     * @param {MouseEvent} ev
     */
    on_save_as: function (ev) {
        ev.stopPropagation();
    },

});

 Registry.add('pdf_cropper_viewer', FieldPdfCropperViewer)

});
