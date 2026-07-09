# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class TransporteDistancias(models.Model):
    _name = 'sicpro.app.transporte.distancia'
    _description = 'Cálculo de Distancias para el Transporte'
    _order = 'name asc'

    name = fields.Char(string='Lugar', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)


class TransporteDistanciasSalida(models.Model):
    _name = 'sicpro.app.transporte.distancia.salida'
    _description = 'Cálculo de Distancias de salida para el Transporte'
    _order = 'name asc'

    name = fields.Many2one(comodel_name='sicpro.app.transporte.distancia',
        string='Salida', required=True)
    destino = fields.Many2one(comodel_name='sicpro.app.transporte.distancia',
        string='Destino', required=True)
    recorrido = fields.Char(string='Recorrido', required=True)
    km = fields.Float(string='Distancia(KM)', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('destino', 'name')
    def _check_destino_salida(self):
        for item in self:
            if item.name == item.destino:
                raise ValidationError(
                    "La Salida y el Destino no pueden ser iguales.\n\n" + MSG_SOPORTE_SICPRO)

    @api.constrains('km')
    def _check_km(self):
        for item in self:
            if item.km == 0:
                raise ValidationError(
                    "Al recorrido creado debe asignar una distancia en KM.\n\n" + MSG_SOPORTE_SICPRO)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TransporteDistanciasSalida, self).create(vals_list)
        for res in records:
            # Crear registro del destino
            res.env['sicpro.app.transporte.distancia.recorrido'].sudo().create(
                {'name': res.recorrido, 'salida_id': res.name.id,
                 'destino_id': res.destino.id, 'km': res.km, })
            return res
        return None

    def unlink(self):
        data = self.env['sicpro.app.transporte.distancia.recorrido'].search(
            [('name', '=', self.recorrido), ])
        for items in data:
            items.unlink()
        return super(TransporteDistanciasSalida, self).unlink()


class TransporteDistanciasRecorrido(models.Model):
    _name = 'sicpro.app.transporte.distancia.recorrido'
    _description = 'Tabla de apoyo para el recorrido'

    name = fields.Char(string='Recorrido', required=True)
    salida_id = fields.Many2one(comodel_name='sicpro.app.transporte.distancia',
                                string='salida_id', required=False)
    destino_id = fields.Many2one(
        comodel_name='sicpro.app.transporte.distancia', string='Destino_id',
        required=False)
    km = fields.Float(string='Distancia(KM)', required=True)
