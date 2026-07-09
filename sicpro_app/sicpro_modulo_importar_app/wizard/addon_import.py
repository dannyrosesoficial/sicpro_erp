# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import io
import shutil
import base64
import zipfile
import tempfile
from pathlib import Path
from odoo.tools import config
from odoo import api, fields, models
from odoo.addons.sicpro_modulo_importar_app.manager import get_tmp_folder_modules


class ModuleIntegrationWizard(models.TransientModel):
    _name = "addon.import.wizard"
    _description = "Asistente de integración de módulos"

    module_file = fields.Binary(string="Archivo de módulo (Zip)")

    def _default_no_addons_path(self):
        addons_string = config.get("addons_path")
        return False if addons_string else True

    no_addons_path = fields.Boolean(
        string="Sin ruta de complementos", default=_default_no_addons_path
    )

    custom_addons_path = fields.Char(string="Ruta de complementos personalizados")

    def _default_addons_path(self):
        addons_string = config.get("addons_path")
        if not addons_string:
            return ""
        return (
            addons_string[0]
            if isinstance(addons_string, list)
            else addons_string.split(",")[0]
        )

    path = fields.Selection(
        string="Ruta del módulo",
        selection="_get_dynamic_path_options",
        default=_default_addons_path,
    )

    overwrite_existing_module = fields.Boolean(
        string="Reemplazar si ya existe", default=True
    )

    def _get_dynamic_path_options(self):
        addons_string = config.get("addons_path")
        addons = (
            addons_string
            if isinstance(addons_string, list)
            else addons_string.split(",") if addons_string else []
        )
        return [(addon, addon) for addon in addons]

    @api.model
    def get_integration_wizard_action(self):
        action = self.env.ref("sicpro_modulo_importar_app.module_integration_wizard").read()[
            0
        ]
        return action

    def from_zip_file(self):
        binary_zip_data = base64.b64decode(self.module_file)
        uploaded_addons_tmp_path = tempfile.mkdtemp(prefix="zip_extract_")

        with zipfile.ZipFile(io.BytesIO(binary_zip_data)) as zf:
            zf.extractall(uploaded_addons_tmp_path)

        addons_path = self.custom_addons_path if self.no_addons_path else self.path
        addons = get_tmp_folder_modules(uploaded_addons_tmp_path)

        return (addons_path, addons, uploaded_addons_tmp_path)

    def confirm_integration(self):
        addons_path, addons, uploaded_addons_tmp_path = self.from_zip_file()

        for module in addons:
            module_path = Path(uploaded_addons_tmp_path) / module
            full_module_dest_path = Path(addons_path) / module

            if self.overwrite_existing_module:
                if full_module_dest_path.exists():
                    shutil.rmtree(full_module_dest_path)

            try:
                shutil.move(str(module_path), str(full_module_dest_path))
            except Exception:
                pass

        ir_module = self.env["ir.module.module"].sudo()
        ir_module.update_list()

        uploaded_addons = ir_module.sudo().search([("name", "in", addons)])
        uploaded_addons.write({"is_uploaded": True})
        uploaded_addons.refresh_logos()
        self.env.cr.commit()

        return {
            "type": "ir.actions.act_window",
            "name": "Aplicaciones",
            "target": "current",
            "res_model": "ir.module.module",
            "views": [[False, "kanban"], [False, "list"], [False, "form"]],
            "context": {},
            "domain": [("name", "in", addons)],
        }
