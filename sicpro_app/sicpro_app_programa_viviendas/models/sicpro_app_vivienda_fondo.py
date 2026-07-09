# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import json
from random import randint
from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ViviendaFondo(models.Model):
    _name = 'sicpro.app.vivienda.fondo'
    _description = 'Presupuesto de fondo para el programa de la vivienda'

    name = fields.Many2one(comodel_name='sicpro.app.vivienda.etapas',
                           string='Etapa', required=True)
    user_id = fields.Many2one('res.users', string='Creado por', index=True,
                              copy=False, default=lambda self: self.env.uid)
    fecha_inicio = fields.Date(string="Fecha inicial", required=True,
                               default=lambda self: fields.Datetime.now())
    active = fields.Boolean(string='Activo', default=True, index=True)
    oferta = fields.Boolean(string='Oferta', required=False, default=False)
    factura = fields.Boolean(string='Factura', required=False, default=False)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id)
    importe = fields.Monetary(string='Importe', currency_field='currency_id',
                              compute='compute_importe')
    saldo = fields.Monetary(string='Saldo', required=False,
                            currency_field='currency_id')
    dominio_materiales = fields.Char(compute="_compute_get_material",
                                     readonly=True, store=False, copy=False)
    material_id = fields.Many2one('sicpro.app.vivienda.materiales',
                                  string='Material', required=True)
    proveedor_id = fields.Many2one('sicpro.app.vivienda.proveedor',
                                   'Proveedor',
                                   related='ofertas_id.proveedor_id',
                                   store=True)
    ofertas_id = fields.Many2one('sicpro.app.vivienda.ofertas',
                                 string='Ofertas',
                                 domain="[('etapa_id', '=', name),]", )
    fecha = fields.Date(string="Fecha", required=True,
                        default=lambda self: fields.Datetime.now())
    estado = fields.Selection(string='Estado', default='pendiente',
                              required=True,
                              selection=[('pendiente', 'Pendiente'), (
                              'pago_anticipado', 'Pago Anticipado'),
                                         ('facturado', 'Facturado'), ])
    trabajadores = fields.Char(string='Beneficiado', compute='compute_importe')
    cantidad_materiales = fields.Char(string='Cant. Mat',
                                      compute='compute_importe')
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.model
    @api.depends('ofertas_id')
    def _compute_get_material(self):
        dic = []
        for item in self:
            material = self.env[
                'sicpro.app.vivienda.trabajador.productos'].sudo().search(
                ['&', '&', ('active', '=', True),
                 ('ofertas_id', '=', item.ofertas_id.id),
                 ('estado', '=', 'entregado')])
            if material:
                for value in material:
                    dic.append(value.name.id)
            item.dominio_materiales = json.dumps([('id', 'in', dic)])

    @api.depends('ofertas_id', 'material_id')
    def compute_importe(self):
        for value in self:
            if value.ofertas_id and value.material_id:
                importe = 0
                trabajadores = 0
                cantidad_materiales = 0
                datos = self.env[
                    'sicpro.app.vivienda.trabajador.productos'].search(
                    ['&', '&', ('ofertas_id', '=', value.ofertas_id.id),
                     ('name', '=', value.material_id.id),
                     ('estado', '=', 'entregado')])
                for item in datos:
                    trabajadores += 1
                    cantidad_materiales += item.cantidad
                    importe += item.total_individual

                value.importe = importe
                value.cantidad_materiales = str(
                    cantidad_materiales) + ' ' + value.material_id.um.name
                if trabajadores == 1:
                    value.trabajadores = str(trabajadores) + ' ' + 'Trabajador'
                else:
                    value.trabajadores = str(
                        trabajadores) + ' ' + 'Trabajadores'
            else:
                value.importe = 0
                value.trabajadores = 0
                value.cantidad_materiales = 0

    @api.constrains('ofertas_id', 'material_id')
    def _check_oferta_material_unico(self):
        if self.ofertas_id and self.material_id:
            uniq = self.env['sicpro.app.vivienda.fondo'].search(
                ['&', '&', ("active", "=", True),
                 ("ofertas_id", "=", self.ofertas_id.id),
                 ("material_id", "=", self.material_id.id),
                 ("id", "!=", self.id), ])
            if uniq:
                raise ValidationError(
                    "¡La oferta y el material introducido ya existe!.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            raise ValidationError(
                "¡Para continuar debe introducir una oferta y materials asignados!.\n\n" + MSG_SOPORTE_SICPRO)

    @api.onchange('oferta', 'factura')
    def compute_oferta_factura(self):
        for item in self:
            if not item.factura and item.oferta:
                item.estado = 'pago_anticipado'
            elif item.factura and item.oferta:
                item.estado = 'facturado'
            else:
                item.estado = 'pendiente'

    def generar_saldo(self):
        asignado = self.env['sicpro.app.vivienda.etapas'].search(
            [('id', '=', self.name.id), ]).monto
        fondo = self.env['sicpro.app.vivienda.fondo'].search(
            [('name', '=', self.name.id), ])
        saldo = 0
        for item in fondo:
            saldo += item.importe
        self.saldo = (asignado - saldo)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(ViviendaFondo, self).create(vals_list)
        for res in records:
            fondo = self.env['sicpro.app.vivienda.fondo'].search(
                ['&', '&', ('name', '=', res.name), ('saldo', '=', 0),
                 ("id", "!=", res.id)])
            if fondo:
                raise ValidationError(
                    "¡No se puede continuar, existen registros sin validar!. "
                    "Si cree que es un error contacte al administrador\n\n" + MSG_SOPORTE_SICPRO)
            return res
        return None
