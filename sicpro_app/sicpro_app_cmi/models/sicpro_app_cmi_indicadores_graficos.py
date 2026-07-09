# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from random import randint
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api


class AppCMIIndicadoresGraficos(models.Model):
    _name = 'sicpro.app.cmi.indicadores.graficos'
    _order = "id asc"
    _description = 'Gráficos de los Indicadores del CMI'

    name = fields.Integer(string='Mes', required=False)
    valor = fields.Integer(string='Valor', required=False)
    tipo = fields.Selection(string='Tipo',
                            selection=[('meta', 'Meta'), ('real', 'Real'), ],
                            required=False, )
    real_pivot = fields.Integer(string='Real', required=False)
    meta_pivot = fields.Integer(string='Meta', required=False)
    porciento_pivot = fields.Integer(string='%', required=False)
    nombre = fields.Char(string='Nombre', required=False)

    mes = fields.Selection(
        [('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'),
         ('abril', 'Abril'), ('mayo', 'Mayo'), ('junio', 'Junio'),
         ('julio', 'Julio'), ('agosto', 'Agosto'),
         ('septiembre', 'Septiembre'), ('octubre', 'Octubre'),
         ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre')],
        string='Meses', )

    @api.model
    def create(self, vals):
        res = super(AppCMIIndicadoresGraficos, self).create(vals)
        for item in res:
            if item.mes == 'enero':
                res['name'] = 1
            if item.mes == 'febrero':
                res['name'] = 2
            if item.mes == 'marzo':
                res['name'] = 3
            if item.mes == 'abril':
                res['name'] = 4
            if item.mes == 'mayo':
                res['name'] = 5
            if item.mes == 'junio':
                res['name'] = 6
            if item.mes == 'julio':
                res['name'] = 7
            if item.mes == 'agosto':
                res['name'] = 8
            if item.mes == 'septiembre':
                res['name'] = 9
            if item.mes == 'octubre':
                res['name'] = 10
            if item.mes == 'noviembre':
                res['name'] = 11
            if item.mes == 'diciembre':
                res['name'] = 12
        return res
