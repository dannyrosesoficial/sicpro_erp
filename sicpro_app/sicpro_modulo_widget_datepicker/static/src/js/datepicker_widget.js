/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component, useRef, onMounted } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class DatePickerField extends Component {
    static template = 'FieldDateMultipleDate';

    setup() {
        // Referencia para el elemento de entrada.
        this.input = useRef("inputdate");

        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            refName: "inputdate",
        });

        onMounted(() => {
            this.initializeFlatpickr();
        });
    }

    // Inicialice el selector de fechas Flatpickr con selección de fechas múltiples
    initializeFlatpickr() {
        if (this.input.el && !this.fpInstance) {
            this.fpInstance = flatpickr(this.input.el, {
                mode: "multiple",
                dateFormat: "Y-m-d",
                defaultDate: this.props.record.data[this.props.name]
                    ? this.props.record.data[this.props.name].split(",")
                    : [],
                onChange: (selectedDates) => {
                    const newValue = selectedDates.map(d => d.toISOString().split("T")[0]).join(",");
                    if (this.props.record.data[this.props.name] !== newValue) {
                        this.props.record.update({
                            [this.props.name]: newValue,
                        });
                    }
                },
            });
        }
    }


    // Manejar el evento de clic para activar Flatpickr en el campo de entrada
    _onSelectDateField(ev) {
        if (!this.input.el._flatpickr) {
            this.initializeFlatpickr();
        }
        this.input.el.focus();
    }
}

// Definir los accesorios del componente.
DatePickerField.props = {
    ...standardFieldProps,
};

// Registrar el campo personalizado en el registro de Odoo
export const datepickerField = {
    component: DatePickerField,
    supportedTypes: ["char"],
};

registry.category("fields").add("multiple_datepicker", datepickerField);
