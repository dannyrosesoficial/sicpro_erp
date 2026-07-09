/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import SurveyPreloadImageMixin from "@survey/js/survey_preload_image_mixin";

publicWidget.registry.SurveyForm = publicWidget.Widget.extend(SurveyPreloadImageMixin, {
    selector: '.o_survey_form',
    events: {
        'focus .o_select_Country': '_onSelectCountry',
        'change .o_select_Country': '_onSelectState',
        'change .o_select_many2many': '_onSelectMany2many',
    },

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
    },

    /**
     * Carga la lista de países mediante RPC y puebla el select.
     */
    _onSelectCountry: async function (ev) {
        const selectElement = ev.target;
        // Evitamos recargar si ya tiene opciones (excepto la inicial)
        if (selectElement.options.length > 1) return;

        try {
            const result = await this.rpc('/survey/load_country', {});
            if (result && result.id) {
                let optionsHtml = '<option value="">País...</option>';
                result.id.forEach((id, index) => {
                    const name = result.name[index];
                    optionsHtml += `<option value="${name}">${name}</option>`;
                });
                selectElement.innerHTML = optionsHtml;
            }
        } catch (error) {
            console.error("Error cargando países:", error);
        }
    },

    /**
     * Carga los estados/provincias basados en el país seleccionado.
     */
    _onSelectState: async function (ev) {
        const country_id = ev.target.value;
        const question_id = ev.target.dataset.id;
        const stateSelect = this.el.querySelector(`#${question_id}-state`);

        if (!stateSelect) return;

        try {
            const result = await this.rpc('/survey/load_states', {
                country_id: country_id,
            });

            let optionsHtml = '<option value="">Estado / Provincia...</option>';
            if (result && result.id) {
                result.id.forEach((id, index) => {
                    const name = result.name[index];
                    optionsHtml += `<option value="${name}">${name}</option>`;
                });
            }
            stateSelect.innerHTML = optionsHtml;
        } catch (error) {
            console.error("Error cargando estados:", error);
        }
    },

    /**
     * Actualiza el campo de texto oculto para respuestas many2many.
     */
    _onSelectMany2many: function (ev) {
        const many2manySelect = ev.target;
        const targetInput = this.el.querySelector('.o_select_many2many_text');
        if (targetInput) {
            // Odoo 19: Obtenemos los valores seleccionados del select múltiple
            const selectedValues = Array.from(many2manySelect.selectedOptions).map(opt => opt.value);
            targetInput.value = JSON.stringify(selectedValues);
        }
    }
});

export default publicWidget.registry.SurveyForm;