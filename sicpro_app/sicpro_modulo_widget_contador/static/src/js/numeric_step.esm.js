/** @odoo-module **/

import { IntegerField, integerField } from "@web/views/fields/integer/integer_field";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

export class NumericStep extends IntegerField {
    static template = "sicpro_modulo_widget_contador.NumericStep";

    _onInputChange(ev) {
        const val = parseInt(ev.target.value) || 0;
        this._applyValue(val);
    }

    _onStepClick(ev) {
        const mode = ev.currentTarget.dataset.mode;
        // Acceso seguro a los datos del registro en Odoo
        const currentValue = this.props.record.data[this.props.name] || 0;
        const step = this.props.step || 1;

        const newValue = mode === "plus" ? currentValue + step : currentValue - step;
        this._applyValue(newValue);
    }

    async _applyValue(val) {
        let finalVal = val;
        // Validaciones de límites
        if (this.props.min !== undefined && finalVal < this.props.min) finalVal = this.props.min;
        if (this.props.max !== undefined && finalVal > this.props.max) finalVal = this.props.max;

        // Actualización estándar del ORM
        await this.props.record.update({ [this.props.name]: finalVal });
    }
}

export const numericStep = {
    ...integerField,
    component: NumericStep,
    displayName: _t("Numeric Step"),
    supportedTypes: ["integer"],
    extractProps: ({ attrs, options }) => ({
        ...integerField.extractProps({ attrs, options }),
        step: parseInt(options.step) || 1,
        min: options.min !== undefined ? parseInt(options.min) : undefined,
        max: options.max !== undefined ? parseInt(options.max) : undefined,
    }),
};

registry.category("fields").add("numeric_step", numericStep);