# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import UserError


class TrabajadoresProteccionTrabajador(models.Model):
    _name = 'sicpro.app.trabajadores.seguridad.trabajador'
    _description = 'Módulo de Seguridad para los trabajadores'
    _order = "anio desc, name asc"

    name = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.seguridad.proteccion',
        string='Descripción', required=False, domain="[('cargo', '=', cargo)]")
    talla = fields.Many2one('sicpro.app.trabajadores.tallas', string='Talla',
                            required=False)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores', required=False)
    codigo = fields.Char(string='Código', related='name.codigo', store=True)
    vida_util = fields.Char(string='Vida Util', related='name.vida_util',
                            store=True)
    unida_medida = fields.Char(string='Unidad de Medidas', store=True,
                               related='name.unida_medida')
    cargo_get = fields.Integer(string='Cargo_get', required=False)
    cargo = fields.Many2one('sicpro.app.trabajadores.cargos',
                            string="Cargo Asociado", required=True,
                            default=lambda self: self.env.context.get(
                                'default_cargo_get'))
    demanda = fields.Integer(string='Demanda', required=False)
    entregado = fields.Integer(string='Entregado', required=False)
    anio = fields.Many2one(comodel_name='sicpro.nomenclador.anios',
                           string='Año', required=True)
    company_id = fields.Many2one('res.company', string='Proceso', store=True,
                                 related='trabajador_id.company_id')
    departamento = fields.Many2one('sicpro.app.trabajadores.areas',
                                   string="Area", required=False, store=True,
                                   related="trabajador_id.area_id")
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True, store=True)
    precio = fields.Monetary(string="Precio", currency_field='company_currency_id',
                             related='name.precio', store=True)

    # verífica que la entrega no sea mayor a la demanda
    @api.depends('demanda')
    @api.onchange('entregado')
    def _onchange_entregado(self):
        if self.demanda < self.entregado:
            self.demanda = None
            raise UserError(
                "El valor de la entrega supera a la demanda. Verifíquelo.\n\n" + MSG_SOPORTE_SICPRO)
