/**  @odoo-module **/

import FormController from 'web.FormController';
import FormView from 'web.FormView';
import viewRegistry from 'web.view_registry';
import core from 'web.core';

var ajax = require('web.ajax');
var qweb = core.qweb;
var _t = core._t;
let res_id
let pdf_firmado_id

var FirmaBotonesControlController = FormController.extend({

    start: function () {
        var sup_ready = this._super.apply(this, arguments);
        sup_ready.then(() => {
            $(document).ready(function () {
                // busco el valor del estado del registro
                let estados_Value = document.getElementsByClassName("js_firma_estados")[0].innerText;
                // busco el valor del id del registro
                res_id = document.getElementsByClassName("js_firma_id")[0].innerText;
                // busco el valor del id del documento firmado
                pdf_firmado_id = document.getElementsByClassName("js_firma_pdf_firmado")[0].innerText;


                // según el estado muestro u oculto los botones del controller
                if (estados_Value === 'Preparación') {
                    $(".o_firma_seleccion").show();
                    $(".o_firma_firmar").hide();
                    $(".o_firma_cancelar").hide();
                    $(".o_firma_descargar_doc").hide();
                } else if (estados_Value === 'Gestión de Firma') {
                    $(".o_firma_seleccion").hide();
                    $(".o_firma_firmar").show();
                    $(".o_firma_cancelar").show();
                    $(".o_firma_descargar_doc").hide();
                } else if (estados_Value === 'Firmado') {
                    $(".o_firma_seleccion").hide();
                    $(".o_firma_firmar").hide();
                    $(".o_firma_cancelar").hide();
                    $(".o_form_button_edit").hide();
                    $(".o_firma_descargar_doc").show();
                } else {

                }


            })

        });
    },

    _ExecuteSeleccion: function () {
        // ejecuto el wizard y envío el id del registro
        this.do_action({
            res_model: "sicpro.app.firma.documentos.wizard",
            name: _t("Seleccionar Página y Área de Firma del Documento"),
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            target: "new",
            context: {default_doc_id: parseInt(res_id), doc_id: parseInt(res_id),},
        });

    },

    _ExecuteFirma: function () {
        // ejecuto el wizard y envío el id del registro
        this.do_action({
            res_model: "sicpro.app.firma.wizard",
            name: _t("Seleccionar Firma Digital"),
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            target: "new",
            context: {default_doc_id: parseInt(res_id), doc_id: parseInt(res_id),},
        });
    },

    _ExecuteCancelarSeleccion: function () {
        // busco la url actual y obtengo el id del registro
        // const url = window.location.href;
        // const paramsString = url.split("#")[1];
        // const paramsArray = paramsString.split("&");
        // var params
        // paramsArray.forEach(param => {
        //     const [key, value] = param.split("=");
        //     if (key === 'id') {
        //         params = value
        //     }
        // });

        // ejecuto el método de python y en vio el id del registro actual
        var self = this;
        self._rpc({
            model: 'sicpro.app.firma.documentos',
            method: 'cancelar_cuadro_firma',
            args: [{}, res_id]
        })
        // recargo la pagina
        location.reload();
    },

    _ExecuteDescargarDoc: function (e) {
        // descargo el documento firmado
        e.preventDefault();
        window.location = '/web/content/' + pdf_firmado_id + '?download=true';
    },


    renderButtons: function ($node) {
        var $footer = this.footerToButtons ? this.renderer.$el && this.renderer.$('footer') : null;
        var mustRenderFooterButtons = $footer && $footer.length;
        if ((this.defaultButtons && !this.$buttons) || mustRenderFooterButtons) {
            this.$buttons = $('<div/>');
            if (mustRenderFooterButtons) {
                this.$buttons.append($footer);
            } else {
                this.$buttons.append(qweb.render("template_firma_botones_control", {widget: this}));
                this.$buttons.on('click', '.o_form_button_edit', this._onEdit.bind(this));
                this.$buttons.on('click', '.o_form_button_create', this._onCreate.bind(this));
                this.$buttons.on('click', '.o_form_button_save', this._onSave.bind(this));
                this.$buttons.on('click', '.o_form_button_cancel', this._onDiscard.bind(this));
                this.$buttons.on('click', '.o_firma_seleccion', this._ExecuteSeleccion.bind(this));
                this.$buttons.on('click', '.o_firma_firmar', this._ExecuteFirma.bind(this));
                this.$buttons.on('click', '.o_firma_cancelar', this._ExecuteCancelarSeleccion.bind(this));
                this.$buttons.on('click', '.o_firma_descargar_doc', this._ExecuteDescargarDoc.bind(this));
                this._assignSaveCancelKeyboardBehavior(this.$buttons.find('.o_form_buttons_edit'));
                this.$buttons.find('.o_form_buttons_edit').tooltip({
                    delay: {show: 200, hide: 0},
                    title: function () {
                        return qweb.render('SaveCancelButton.tooltip');
                    },
                    trigger: 'manual',
                });
            }
        }
        if (this.$buttons && $node) {
            this.$buttons.appendTo($node);
        }
    },
});


var FirmaBotonesControlFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: FirmaBotonesControlController,
    }),
});

viewRegistry.add('firma_botones_control', FirmaBotonesControlFormView);