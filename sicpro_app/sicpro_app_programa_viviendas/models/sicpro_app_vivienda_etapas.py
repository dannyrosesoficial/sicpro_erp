# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api


def _default_color():
    return randint(1, 11)


class ViviendaEtapas(models.Model):
    _name = "sicpro.app.vivienda.etapas"
    _description = "Etapas del programa de la vivienda"

    name = fields.Char('Etapa', required=True)
    active = fields.Boolean('Activo', default=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id',
                                       readonly=True)
    monto = fields.Monetary(currency_field='company_currency', string="Presupuesto Asignado", required=True)
    monto_usado = fields.Monetary(currency_field='company_currency', string="Presupuesto Usado",
                                  compute='compute_montos')
    monto_restante = fields.Monetary(currency_field='company_currency', string="Presupuesto Restante",
                                     compute='compute_montos')
    pago_anticipado = fields.Monetary(currency_field='company_currency', string="Pago Anticipado",
                                      compute='compute_montos')
    fecha_inicio = fields.Date(string='Inicio de la etapa', required=True)
    vencimiento_presupuesto = fields.Date(string='Vencimiento del presupuesto', required=True)
    fecha_fin = fields.Date(string='Fin de la etapa')
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    estado = fields.Selection(string='Estado', default='activa', compute='_compute_estado',
                              selection=[('activa', 'Activa'), ('terminada', 'Terminada'), ], required=True, )
    terminado = fields.Boolean(string='Terminado', required=False, default=False)

    @api.onchange('fecha_fin')
    def _compute_estado(self):
        for item in self:
            if item.fecha_fin:
                item.estado = 'terminada'
                item.terminado = True
            else:
                item.estado = 'activa'
                item.terminado = False

    def compute_montos(self):
        for value in self:
            usado = 0
            anticipado = 0
            fondo_usado = self.env['sicpro.app.vivienda.fondo'].search(
                [('name', '=', value.id), ('estado', 'in', ['pago_anticipado', 'facturado'])])

            if fondo_usado:
                for item in fondo_usado:
                    usado += item.importe

                fondo_anticipado = self.env['sicpro.app.vivienda.fondo'].search(
                    [('name', '=', value.id), ('estado', '=', 'pago_anticipado')])
                for item in fondo_anticipado:
                    anticipado += item.importe

                value.monto_usado = usado
                value.monto_restante = (value.monto - usado)
                value.pago_anticipado = anticipado
            else:
                value.monto_usado = usado
                value.monto_restante = 0
                value.pago_anticipado = anticipado

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "¡La etapa ya existe!"),
    ]
