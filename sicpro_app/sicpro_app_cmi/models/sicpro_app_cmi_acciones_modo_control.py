# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from random import randint
from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


def _default_color():
    return randint(1, 11)


class AppCMIAccionesModoControl(models.Model):
    _name = 'sicpro.app.cmi.acciones.modo.control'
    _order = "id asc"
    _description = 'Modo de Control de las acciones'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError("¡El nombre de control '%s' ya existe en el sistema!\n\n" % record.name + MSG_SOPORTE_SICPRO)
