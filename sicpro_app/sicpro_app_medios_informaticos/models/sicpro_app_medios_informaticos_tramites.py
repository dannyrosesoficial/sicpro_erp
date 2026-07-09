# -*- coding: utf-8

from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO


class MediosInformaticosTipoEquipo(models.Model):
    _name = 'sicpro.app.medios.informaticos.tramites'
    _description = "Trámites del taller de Medio Informático"

    name = fields.Char(string='Trámite', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El nombre del trámite '%s' ya existe en el sistema!" % record.name + MSG_SOPORTE_SICPRO)
