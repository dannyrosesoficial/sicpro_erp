# -*- coding: utf-8 -*-

from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        res = super().session_info()
        allowed_group = "sicpro_modulo_importar_seguridad.group_import_csv"
        allowed_group_id = request.env.ref(allowed_group, raise_if_not_found=False)
        if not allowed_group_id or request.env.user.has_group(allowed_group):
            res["sicpro_modulo_importar_seguridad__allow_import"] = 1
        return res
