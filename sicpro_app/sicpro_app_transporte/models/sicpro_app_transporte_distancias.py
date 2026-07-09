# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class TransporteDistancias(models.Model):
    _name = 'sicpro.app.transporte.distancia'
    _description = 'Cálculo de Distancias para el Transporte'
    _order = 'name asc'

    name = fields.Char('Lugar', required=True)
    active = fields.Boolean(default=True)


class TransporteDistanciasSalida(models.Model):
    _name = 'sicpro.app.transporte.distancia.salida'
    _description = 'Cálculo de Distancias de salida para el Transporte'
    _order = 'name asc'

    name = fields.Many2one(
        comodel_name='sicpro.app.transporte.distancia',
        string='Salida', required=True)
    destino = fields.Many2one(
        comodel_name='sicpro.app.transporte.distancia',
        string='Destino', required=True)
    recorrido = fields.Char('Recorrido', required=True)
    km = fields.Float(string='Distancia(KM)', required=True)
    active = fields.Boolean(default=True)

    @api.constrains('destino', 'name')
    def _check_destino_salida(self):
        for item in self:
            if item.name == item.destino:
                raise ValidationError(
                    _("La Salida y el Destino no pueden ser iguales."))

    @api.constrains('km')
    def _check_km(self):
        for item in self:
            if item.km == 0:
                raise ValidationError(
                    _("Al recorrido creado debe asignar una distancia en KM."))

    @api.model
    def create(self, vals):
        item = super(TransporteDistanciasSalida, self).create(vals)
        # Crear registro del destino
        item.env['sicpro.app.transporte.distancia.recorrido'].sudo().create(
            {'name': item.recorrido,
             'salida_id': item.name.id,
             'destino_id': item.destino.id,
             'km': item.km,
             })
        return item

    def unlink(self):
        data = self.env['sicpro.app.transporte.distancia.recorrido'].search(
            [('name', '=', self.recorrido), ])
        for items in data:
            items.unlink()
        return super(TransporteDistanciasSalida, self).unlink()


class TransporteDistanciasRecorrido(models.Model):
    _name = 'sicpro.app.transporte.distancia.recorrido'
    _description = 'Tabla de apoyo para el recorrido'

    name = fields.Char('Recorrido', required=True)
    salida_id = fields.Many2one(comodel_name='sicpro.app.transporte.distancia',
                                string='salida_id', required=False)
    destino_id = fields.Many2one(comodel_name='sicpro.app.transporte.distancia',
                                 string='Destino_id', required=False)
    km = fields.Float(string='Distancia(KM)', required=True)
