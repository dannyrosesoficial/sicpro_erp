# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api


class SicproWebEquipo(models.Model):
    _name = 'sicpro.modulo.web.equipo'
    _description = 'Equipo de Desarrollo'
    _order = "sequence, id"

    name = fields.Char(string='Nombre', required=True)
    cargo = fields.Char(string='Cargo', required=True)
    responsabilidad = fields.Html(string='Responsabilidad', required=True)

    # Redes Sociales
    cuenta_twitter = fields.Char(string='Twitter')
    cuenta_facebook = fields.Char(string='Facebook')
    cuenta_instagram = fields.Char(string='Instagram')
    cuenta_linkedin = fields.Char(string='Linkedin')
    cuenta_correo = fields.Char(string='Correo')
    cuenta_gitlab = fields.Char(string='Gitlab')

    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    image_1920 = fields.Image("Imagen", max_width=1024, max_height=1024)

    @api.model
    def buscar_datos_equipos(self):
        # Usamos sudo() para acceso público
        equipos = self.sudo().search([('active', '=', True)])
        equipos_list = []

        for item in equipos:
            equipos_list.append({'nombre': item.name, 'cargo': item.cargo,
                                 'responsabilidad': item.responsabilidad,
                                 'twitter': item.cuenta_twitter,
                                 'facebook': item.cuenta_facebook,
                                 'instagram': item.cuenta_instagram,
                                 'linkedin': item.cuenta_linkedin,
                                 'correo': item.cuenta_correo,
                                 'gitlab': item.cuenta_gitlab,
                                 # URL simplificada y directa
                                 'imagen': f'/web/image/sicpro.modulo.web.equipo/{item.id}/image_1920'})
        return equipos_list
