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
from odoo.exceptions import ValidationError


class Trabajos(models.Model):
    _name = "sicpro.app.trabajadores.ocupacion"
    _description = "Categoría Ocupacional del trabajador"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'area_sequence, id'

    name = fields.Many2one(comodel_name='sicpro.app.trabajadores.cargos',
                           string='Categoría Ocupacional', required=True)
    active = fields.Boolean(string="Activo", default=True, )
    cantidad_trabajadores = fields.Integer(
        compute='_compute_cuenta_trabajadores',
        string="Cantidad de trabajadores", store=True, )
    descripcion = fields.Text(string='Descripción del trabajo')
    area_id = fields.Many2one('sicpro.app.trabajadores.areas',
                              string='Departamento', required=True, )
    area_sequence = fields.Integer(related='area_id.departamento_sequence',
                                   store=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 readonly=True, store=True,
                                 related='area_id.company_id', )
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    trabajadores_ids = fields.One2many('sicpro.app.trabajadores',
                                       'ocupacion_id', string='Trabajadores', )
    salario = fields.Monetary(string="Salario", currency_field='company_currency_id',
                              related='name.salario', store=True, )
    alimentacion = fields.Monetary(string="Alimentación",
                                   currency_field='company_currency_id',
                                   related='name.alimentacion', store=True, )

    @api.constrains('name', 'company_id', 'area_id')
    def _check_unique_puesto_trabajo(self):
        for record in self:
            if not record.name or not record.area_id or not record.company_id:
                continue
            puesto_nombre = record.name.display_name
            domain = [('name', '=', record.name.id),
                      # Comparación por ID (Más rápido y seguro)
                      ('company_id', '=', record.company_id.id),
                      ('area_id', '=', record.area_id.id),
                      ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡Error de Duplicidad! Ya existe el puesto de trabajo '%s' "
                    "asignado al departamento/área '%s' dentro de la compañía '%s'." % (
                        puesto_nombre, record.area_id.display_name,
                        record.company_id.name) + MSG_SOPORTE_SICPRO)

    # Cuenta la cantidad de trabajadores existentes en la categoría
    @api.depends('trabajadores_ids.ocupacion_id', 'trabajadores_ids.active')
    def _compute_cuenta_trabajadores(self):
        trabajadores_data = self.env['sicpro.app.trabajadores'].read_group(
            [('ocupacion_id', 'in', self.ids)], ['ocupacion_id'],
            ['ocupacion_id'])
        result = dict(
            (data['ocupacion_id'][0], data['ocupacion_id_count']) for data in
            trabajadores_data)
        for ocupacion in self:
            ocupacion.cantidad_trabajadores = result.get(ocupacion.id, 0)

    @api.model_create_multi
    def create(self, vals_list):
        return super(Trabajos,
                     self.with_context(mail_create_nosubscribe=True)).create(
            vals_list)

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = "%s (copia)" % (self.name or '')
        return super(Trabajos, self).copy(default=default)
