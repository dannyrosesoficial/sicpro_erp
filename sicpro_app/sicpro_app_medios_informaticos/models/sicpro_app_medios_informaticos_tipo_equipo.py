# -*- coding: utf-8

from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO


class MediosInformaticosTipoEquipo(models.Model):
    _name = 'sicpro.app.medios.informaticos.tipo.equipo'
    _description = "Tipo de Medio Informático"

    name = fields.Char(string='Tipo de Equipo', required=True, )
    active = fields.Boolean(string='Activo', default=True, index=True)
    imagen = fields.Image('Imagen')

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El Tipo Equipo '%s' ya existe!\n\n" % record.name + MSG_SOPORTE_SICPRO)
