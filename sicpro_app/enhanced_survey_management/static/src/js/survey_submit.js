/** @odoo-module **/

import {
    parseDateTime,
    parseDate,
    serializeDateTime,
    serializeDate,
} from "@web/core/l10n/dates";
import SurveyFormWidget from '@survey/js/survey_form';

/**
 * Extensión de SurveyFormWidget para Odoo 19 - SICPRO
 * Se corrige el envío de datos complejos para evitar RPC_ERROR
 */
SurveyFormWidget.include({
    events: Object.assign({}, SurveyFormWidget.prototype.events, {
        'change .o_file': '_onChangeFile',
        'change .o_survey_form_choice_item': '_onChangeChoiceItem',
        'click .o_survey_matrix_btn': '_onMatrixBtnClick',
        'click input[type="radio"]': '_onRadioChoiceClick',
        'click button[type="submit"]': '_onSubmit',
        'click .o_survey_choice_img img': '_onChoiceImgClick',
        'focusin .form-control': '_updateEnterButtonText',
        'focusout .form-control': '_updateEnterButtonText'
    }),

    /**
     * Prepara los valores para el envío al backend.
     * REGLA ODOO 19: Los valores en params deben ser tipos primitivos (Strings/Numbers).
     */
    _prepareSubmitValues: function (formData, params) {
        this._super(...arguments);
        const self = this;

        let address = {};
        let names = {};
        let matrix = {};

        this.$('[data-question-type]').each(function () {
            const $el = $(this);
            const qType = $el.data('questionType');
            const name = this.name;

            // Evitamos procesar si no hay nombre (evita colisiones con inputs decorativos)
            if (!name) return;

            switch (qType) {
                // --- TIPOS SIMPLES ---
                case 'url':
                case 'email':
                case 'week':
                case 'color':
                case 'time':
                case 'range':
                case 'password':
                case 'month':
                case 'selection':
                    params[name] = this.value || "";
                    break;

                // --- RELACIONALES (Convertidos a String para evitar RPC Error) ---
                case 'many2one':
                    // En v19, enviamos solo el ID como string.
                    // El servidor lo guardará en el char_box de la línea de respuesta.
                    params[name] = this.value ? this.value.toString() : "";
                    break;

                case 'many2many':
                    // Convertimos el array de IDs a una cadena separada por comas
                    const m2mValue = $el.val();
                    params[name] = Array.isArray(m2mValue) ? m2mValue.join(',') : (m2mValue || "");
                    break;

                // --- AGRUPADOS: DIRECCIÓN (Aplanado a JSON String) ---
                case 'address':
                    address[name] = this.value;
                    if (name.endsWith('pin')) {
                        const prefix = name.split("-")[0];
                        address[prefix + '-country'] = self.$(`#${prefix}-country`).val();
                        address[prefix + '-state'] = self.$(`#${prefix}-state`).val();
                        // Importante: No enviamos el objeto, enviamos el JSON String
                        params[prefix] = JSON.stringify(address);
                        address = {};
                    }
                    break;

                // --- AGRUPADOS: NOMBRE (Aplanado a JSON String) ---
                case 'name':
                    names[name] = this.value;
                    if (name.endsWith('last')) {
                        const prefix = name.split("-")[0];
                        params[prefix] = JSON.stringify(names);
                        names = {};
                    }
                    break;

                // --- MATRIZ PERSONALIZADA ---
                case 'custom':
                    if (name === 'matrix-end') {
                        params[this.id] = JSON.stringify(matrix);
                        matrix = {};
                    } else if ($el.attr('id') === 'select') {
                        matrix[name] = $el.find("option:selected").data('value');
                    } else {
                        matrix[name] = this.value;
                    }
                    break;

                // --- ARCHIVOS (Base64 plano) ---
                case 'file':
                    const fileBase64 = $el.attr('data-file-name');
                    if (fileBase64) {
                        const fileName = (this.files && this.files[0]) ? this.files[0].name : "archivo";
                        // Enviamos un string compuesto. Formato: name|base64
                        params[name] = fileName + "|" + fileBase64;
                    }
                    break;
            }
        });
    },

    /**
     * Maneja la lectura de archivos y los convierte a Base64.
     */
    _onChangeFile: function (ev) {
        const self = this;
        const element = ev.target;

        if (element.files && element.files[0]) {
            const file = element.files[0];
            const reader = new FileReader();
            const $el = $(element);

            reader.onloadend = function () {
                const base64Data = reader.result.split(',')[1];
                $el.attr('data-file-name', base64Data);
            };
            reader.readAsDataURL(file);
        }
    },
});