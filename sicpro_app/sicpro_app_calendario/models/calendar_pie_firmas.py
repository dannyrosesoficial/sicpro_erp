# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, models, fields
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class MeetingPieFirmas(models.Model):
    _name = 'calendar.pie.firmas'
    _description = 'Pie de Firma del Calendario'

    name = fields.Many2one('res.users', string='Usuario', required=True)
    tipo = fields.Selection(string='Tipo', selection=[('aprueba', 'Aprueba'), (
    'elabora', 'Elabora'), ], required=True, )
    active = fields.Boolean(string='Archivado', required=True, default=True, index=True)

    @api.constrains('tipo')
    def _check_unique_tipo_autorizacion(self):
        for record in self:
            if record.tipo:
                # Buscamos duplicados ignorando mayúsculas y espacios innecesarios
                # Ejemplo: 'Acceso' y 'acceso ' se considerarán iguales
                tipo_limpio = record.tipo.strip()
                duplicate = self.search(
                    [('tipo', '=ilike', tipo_limpio), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Conflicto de Seguridad! El tipo de autorización '%s' ya está registrado. "
                        "Por favor, use un nombre diferente o edite el existente en SICPRO.\n\n" % tipo_limpio + MSG_SOPORTE_SICPRO)
