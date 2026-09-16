# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class NomencladorSindicato(models.Model):
    _name = "sicpro.nomenclador.sindicato"
    _description = "Áreas sindicales de la DVPE"

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Sección Sindical', required=True)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores',
                                    string='Responsable', required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Usuario',
                              related='trabajador_id.user_id')
    areas_ids = fields.One2many('sicpro.app.trabajadores.areas',
                                'seccion_sindical_id', string='Áreas',
                                required=True)
    color = fields.Integer(string='Color',
                           default=_default_color)

    @api.constrains('name')
    def _check_name_insensitive(self):
        for record in self:
            if record.name:
                duplicate = self.search(
                    [('name', '=ilike', record.name), ('id', '!=', record.id)],
                    limit=1)
                if duplicate:
                    raise ValidationError(
                        "¡El nombre de la sección sindical ya existe (sin importar mayúsculas)!.\n\n" + MSG_SOPORTE_SICPRO)
