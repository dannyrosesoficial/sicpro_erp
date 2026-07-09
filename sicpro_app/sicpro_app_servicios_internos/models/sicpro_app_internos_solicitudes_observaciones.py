# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class ServiciosInternosSolicitudesObservaciones(models.Model):
    _name = 'sicpro.app.servicios.internos.solicitudes.observaciones'
    _description = "Gestión de observaciones de las solicitudes"

    active = fields.Boolean(default=True, index=True)
    name = fields.Text(string='Observaciones', required=True)
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('anexo1', 'Anexo 1'),
                                       ('anexo2', 'Anexo 2'), (
                                       'Compromiso_nauta', 'Compromiso Nauta'),
                                       ('Planilla_unica',
                                        'Planilla Única'), ])
