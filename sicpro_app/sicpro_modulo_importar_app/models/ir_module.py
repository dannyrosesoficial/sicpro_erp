# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import os
import sys
import base64
import shutil
import subprocess
from odoo.modules import get_module_path
from odoo import modules, models, fields, tools, exceptions

import logging

LOG = logging.getLogger(__file__)


class IrModule(models.Model):
    _inherit = "ir.module.module"
    _description = "Module"

    is_uploaded = fields.Boolean(string="Está subido", default=False)

    def refresh_logos(self):
        for module in self:
            if not module.id:
                continue
            if module.icon:
                path = os.path.join(module.icon.lstrip("/"))
            else:
                path = modules.module.get_module_icon_path(module)
            if path:
                try:
                    with tools.file_open(
                        path, "rb", filter_ext=(".png", ".svg", ".gif", ".jpeg", ".jpg")
                    ) as image_file:
                        module.icon_image = base64.b64encode(image_file.read())
                except FileNotFoundError:
                    module.icon_image = ""

    def install_python_required_packages(self):
        for rec in self:
            manifest = self.sudo().get_module_info(rec.name)
            depends = manifest.get("external_dependencies", {}).get("python", [])
            try:
                modules.check_manifest_dependencies(manifest)
            except Exception:
                for package in depends:
                    try:
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", package]
                        )
                    except subprocess.CalledProcessError as error:
                        raise exceptions.UserError(
                            f"Unable to install {package} \n {error}"
                        )

    def remove_from_the_addons_directory(self):
        for rec in self:
            if rec.module_type == "uploaded":
                module_path = get_module_path(rec.name, downloaded=False)
                LOG.warning(f"REMOVE: {module_path}")
                rec.sudo().unlink()
                shutil.rmtree(module_path, ignore_errors=False)
