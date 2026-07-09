# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import api, models, fields
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ViviendaOfertas(models.Model):
    _name = 'sicpro.app.vivienda.ofertas'
    _description = 'Ofertas para el programa de la vivienda'

    name = fields.Char(string='Oferta', required=True)
    proveedor_id = fields.Many2one('sicpro.app.vivienda.proveedor',
                                   'Proveedor', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              default=lambda self: self.env.uid)
    etapa_id = fields.Many2one('sicpro.app.vivienda.etapas', string='Etapa',
                               required=True)
    fecha = fields.Date(string="Fecha", required=True,
                        default=lambda self: fields.Datetime.now())
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_unique_offer_name(self):
        for record in self:
            if record.name:
                # Normalizamos: eliminamos espacios y comparamos sin importar mayúsculas
                # Esto evita duplicados como "Promo 10%" y "promo 10% "
                name_clean = record.name.strip()

                duplicate = self.search(
                    [('name', '=ilike', name_clean), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Error de Ventas! Ya existe una oferta con el nombre '%s'. "
                        "Por favor, use un nombre distintivo para la nueva promoción en SICPRO.\n\n" % name_clean + MSG_SOPORTE_SICPRO)

    def archivar(self):
        self.active = False

    def desarchivar(self):
        self.active = True
