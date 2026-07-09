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


class SoporteFragmentosCodigos(models.Model):
    _name = 'sicpro.app.soporte.fragmentos.codigos'
    _description = 'Fragmentos de códigos del desarrollo del sistema'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    DEFAULT_PYTHON_CODE = """# Agregue el fragmento de código:
    # - Aquí puede agregar el fragmento de código que desee recordar
    # - Debe ser un diseño de código genérico que pueda ser modificado según el caso de uso.
    # - Todo el diseño debe venir acompañado de sus respectivos comentarios."""

    active = fields.Boolean(string='Activo', default=True, index=True)
    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Creado por', index=True,
                              required=True, default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    codigo_python = fields.Text(string='Código Python', )
    codigo_xml = fields.Text(string='Código Xml', )
    codigo_otros = fields.Text(string='Otros Códigos', )
    tipo_codigo = fields.Selection(string='Tipos de Código',
                                   selection=[('python', 'Código Python'),
                                              ('xml', 'Código Xml'),
                                              ('otros', 'Otros Códigos'), ],
                                   required=True, )
