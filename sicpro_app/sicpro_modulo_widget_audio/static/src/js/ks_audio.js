/** @odoo-module */

import { registry } from "@web/core/registry";
import { CharField, charField } from "@web/views/fields/char/char_field";

class KsAudio extends CharField {
    static template = "sicpro_modulo_widget_audio.audio_widget";
    static props = {...CharField.props,};
}
export const ksAudio = {...charField, component: KsAudio,};
registry.category("fields").add("ks_audio", ksAudio);
