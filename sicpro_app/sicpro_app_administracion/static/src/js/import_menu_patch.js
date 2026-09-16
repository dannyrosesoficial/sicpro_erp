/** @odoo-module **/
import {registry} from "@web/core/registry";
import {session} from "@web/session";

const cogMenuRegistry = registry.category("cogMenu");

// Esperamos un momento a que Odoo registre sus menús y luego modificamos el de importación
const originalImportItem = cogMenuRegistry.get("import-menu");


const originalIsDisplayed = originalImportItem.isDisplayed;

originalImportItem.isDisplayed = (env) => {
    const odooAllow = originalIsDisplayed(env);
    const sicproAllow = session.can_import === true;
    return odooAllow && sicproAllow;
};

