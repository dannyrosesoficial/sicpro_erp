# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models
from odoo.exceptions import UserError


class PlantillaSoporteBitacora(models.Model):
    _inherit = "sicpro.app.soporte.bitacora"

    tipo_desactivacion = fields.Selection(
        [('ldap', 'Inexistente en LDAP'), ('acceso', 'Inactividad de Acceso'),
         ('registro', 'Sin Primer Inicio de Sesión'),
         ('manual', 'Desactivación Manual')], string='Causa de Desactivación',
        help="Índica qué proceso automático ejecutó la desactivación.",
        default='manual')


