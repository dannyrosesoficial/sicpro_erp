# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    running_python_version = fields.Char(
        default=lambda x: x.get_python_version())

    def get_python_version(self):
        from platform import python_version
        return "Python %s" % python_version()

    def button_open_python_packages(self):
        self.ensure_one()
        self.env['python.paquetes.instalados'].sudo().update_packages()
        return {'type': 'ir.actions.act_window', 'view_mode': 'list',
                'target': 'new', 'res_model': 'python.paquetes.instalados',
                'name': "%s Paquetes Instalados" % self.running_python_version, }
