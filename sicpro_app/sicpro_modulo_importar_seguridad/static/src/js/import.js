odoo.define("sicpro_modulo_importar_seguridad.group_import", function (require) {
    "use strict";

    const ImportMenu = require("base_import.ImportMenu");
    const shouldBeDisplayed_orig = ImportMenu.shouldBeDisplayed;

    ImportMenu.shouldBeDisplayed = function (env) {
        return (
            shouldBeDisplayed_orig(env) &&
            env.session.sicpro_modulo_importar_seguridad__allow_import === 1
        );
    };
});
