# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, date
from random import randint


class ViveresAreasEntregas(models.Model):
    _name = 'sicpro.app.viveres.areas.entregas'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _description = "Entregas por áreas, módulo de víveres"

    def _get_trabajadores_domain(self):
        if self.name.name.tipo_registro == 'sin_categoría':
            trabajadores = self.env['sicpro.app.trabajadores'].search(
                ['&', ('active', '=', True), ('area_id.id', '=', self.name.name.id)])
        else:
            trabajadores = self.env['sicpro.app.trabajadores'].search(
                [('active', '=', True), '|', ('area_id.id', '=', self.name.name.id),
                 ('area_id.parent_id.id', '=', self.name.name.id)])

        list_trabajadores = []
        for trabajador in trabajadores:
            list_trabajadores.append(trabajador.id)

        return [('id', 'in', list_trabajadores)]

    name = fields.Many2one('sicpro.app.viveres.areas', string='Área', required=True)
    direccion = fields.Many2one('res.company', string='Proceso', related='name.direccion', store=True, )
    active = fields.Boolean('Activo', default=True)
    producto_comprado = fields.Many2many('sicpro.app.viveres.productos.comprados', 'sicpro_app_areas_entregas_rel',
                                         'areas_entrega_id', 'producto_comprado_id', required=True, string='Producto', )
    fecha = fields.Date('Fecha entrega')
    total_entregado = fields.Integer('Total entregado')
    total_trabajadores = fields.Integer('Total trabajadores', compute='_compute_total_trabajadores')
    total_no_entregado = fields.Integer('Total no entregado')
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', )
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes')
    anio = fields.Char(string='Año', default=fields.Datetime.now().strftime("%Y"))
    observaciones = fields.Text(string="Observaciones", required=False, )
    trabajador = fields.Many2one('sicpro.app.trabajadores', string='Entregado a', required=True, )
    company_id = fields.Many2one('res.company', string='Procesos', required=True, default=lambda self: self.env.company)

    @api.constrains('fecha')
    def restriccion_fecha_entrega(self):
        if self.fecha:
            today = date.today()
            if self.fecha > today:
                raise UserError('La fecha de entrega no puede ser mayor al día de hoy,'
                                ' verifíquelo. Si cree que es un error contacte al administrador')
            elif self.producto_comprado:
                for producto in self.producto_comprado:
                    if self.fecha < producto.fecha:
                        raise UserError('La fecha de entrega no puede ser menor a la fecha de compra,'
                                        ' verifíquelo. Si cree que es un error contacte al administrador')

    def _get_productos_entregados(self):
        return str([producto.name.name for producto in self.producto_comprado]).replace('[', '').replace(']', '')

    def notificar_nuevo_registro(self):
        # busco el trabajador que recoge los productos
        recoge = self.trabajador.user_id
        # busco los usuarios responsables
        responsables = self.env.ref('sicpro_app_viveres.grupo_app_viveres_areas_responsable').users
        # creo la lista de seguidores
        seguidores = recoge + responsables
        # agrego los seguidores al modelo
        self.message_subscribe(partner_ids=seguidores.partner_id.ids)
        # envió la notificación a los seguidores
        self.message_post(body='Entrega de productos', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        for participante in self.message_partner_ids:
            # envío el correo electrónico
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            template = self.env.ref('sicpro_app_viveres.viveres_entregas_areas')
            template.send_mail(self.id, force_send=True, email_values=email_values, )

    @api.depends("name.name")
    def _compute_total_trabajadores(self):
        hoy = datetime.today()
        mes_anterior, anio = (hoy.month - 1, hoy.year) if hoy.month != 1 else (12, hoy.year - 1)
        for each in self:
            if each:
                area_totales = self.env['sicpro.app.viveres.cierre'].search(
                    ['&', ('name', '=', each.name.id), ('codigo_mes', '=', mes_anterior), ('anio', '=', anio)])

                if area_totales:
                    each.total_trabajadores = area_totales.total
                else:
                    each.total_trabajadores = 0

    @api.model
    def create(self, vals_list):
        res = super(ViveresAreasEntregas, self).create(vals_list)

        for producto in res['producto_comprado']:
            area_producto_comprado = self.env['sicpro.app.viveres.areas.entregas'].search(
                ['&', ('name', '=', res['name'].id), ('producto_comprado', '=', producto.id), ('id', '!=', res['id'])])
            if area_producto_comprado:
                raise UserError('A esta área ya se le entrego este producto,'
                                ' verifíquelo. Si cree que es un error contacte al administrador')

            nombre_mes = self.env['sicpro.nomenclador.meses'].search(
                ['&', ('active', '=', True), ('codigo_mes', '=', res['fecha'].month)])
            res['mes'] = nombre_mes.id
            res['anio'] = res['fecha'].year
            res['total_no_entregado'] = res['total_entregado']

            viveres_producto_comprado = self.env['sicpro.app.viveres'].search([('name', '=', producto.id)])

            if not viveres_producto_comprado:
                self.env['sicpro.app.viveres'].sudo().create({'name': producto.id})

            fondo_entrega = self.env['sicpro.app.viveres.areas.fondo'].search(
                ['&', ('name', '=', res['name'].id), ('codigo_mes', '=', res['fecha'].month),
                 ('anio', '=', res['fecha'].year)])

            if not fondo_entrega:
                self.env['sicpro.app.viveres.areas.fondo'].sudo().create(
                    {'name': res['name'].id, 'mes': nombre_mes.id, 'anio': res['fecha'].year})

            self.env['sicpro.app.viveres.areas.entregas.resumenes'].sudo().create(
                {'name': res['name'].id, 'producto': producto.id})

        res.notificar_nuevo_registro()

        return res

    def write(self, vals):
        res = super(ViveresAreasEntregas, self).write(vals)
        for item in self:
            if vals.get('total_entregado'):
                total = vals['total_entregado']
                item['total_no_entregado'] = total

        return res