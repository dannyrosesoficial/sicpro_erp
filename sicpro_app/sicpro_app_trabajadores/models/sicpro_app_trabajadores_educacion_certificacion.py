# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models


class TrabajadoresEducacionCertificacion(models.Model):
    _name = 'sicpro.app.trabajadores.educacion.certificacion'
    _description = "Certificación y Homologación del trabajador"
    _order = "sequence"
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Nombre de la Empresas Nacional Certificadora de Personas',
        required=True)
    vigencia = fields.Integer(string='Vigencia (Años)', required=True)
    dias = fields.Integer(string='Días', required=False,
                          compute='_compute_dias_vigencia')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)

    @api.depends('vigencia')
    def _compute_dias_vigencia(self):
        for cert in self:
            if cert.vigencia:
                cert.dias = cert.vigencia * 365
            else:
                cert.dias = None
