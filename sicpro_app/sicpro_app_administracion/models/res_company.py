# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


class Company(models.Model):
    _inherit = 'res.company'
    _order = 'id'

    identificador_corto = fields.Char(string="Identificador", required=True, )
    ejecuta_proceso = fields.Boolean(string="Ejecutor de Procesos", )
    login_redes_sociales = fields.Boolean(string="Mostrar Redes Sociales",
                                          default=False)
    link_twitter = fields.Char(string='Usuario X')
    link_facebook = fields.Char(string='Usuario Facebook')
    link_linkedin = fields.Char(string='Usuario LinkedIn')
    link_instagram = fields.Char(string='Usuario Instagram')
    link_dvpe = fields.Char(string='Link DVPE')

    @api.constrains('login_redes_sociales')
    def _check_unique_login_redes(self):
        for record in self:
            if record.login_redes_sociales:
                # Buscamos si existe OTRA compañía que ya tenga esto marcado
                count = self.sudo().search_count([
                    ('login_redes_sociales', '=', True),
                    ('id', '!=', record.id)
                ])
                if count > 0:
                    raise ValidationError(
                        "Ya existe otra compañía con la opción 'Mostrar Redes Sociales' activa. "
                        "Solo se permite tener una compañía configurada para este fin." + MSG_SOPORTE_SICPRO
                    )

    def get_link_sociales(self):
        self.ensure_one()
        return {
            'link_facebook': self.link_facebook,
            'link_linkedin': self.link_linkedin,
            'link_twitter': self.link_twitter,
            'link_instagram': self.link_instagram,
            'link_dvpe': self.link_dvpe,
        }