# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class View(models.Model):
    _inherit = 'ir.ui.view'

    def _render_template(self, template, values=None, engine='ir.qweb'):
        if not values:
            values = {}
        values["title"] = values["app_title"] = self.env[
            'ir.config_parameter'].sudo().get_param("app_system_name",
                                                    "SICPRO ERP")
        return super(View, self)._render_template(template, values=values,
                                                  engine=engine)
