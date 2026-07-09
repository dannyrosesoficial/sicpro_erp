# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PreparacionTecnicaSalario(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.salario'
    _description = 'Salario de la Preparación Técnica'

    def get_total_dias(self):
        return self.env['sicpro.app.preparacion.tecnica.preparaciones'].search(
            [('id', '!=', self._origin.id)], limit=1).total_dias_actividades

    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=True, )

    departamento_id = fields.Many2one(
        'sicpro.app.trabajadores.departmentos', string="Area", )

    categoria_ocupacional_id = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.trabajos", string="Categoría",
        required=True, )
    salario = fields.Monetary("Salario", currency_field='company_currency_id',
                              compute='_compute_salario',
                              compute_sudo=True, store=True, )
    tarifa_horaria = fields.Float(string='Tarifa H.',
                                  compute='_compute_tarifa_horaria',
                                  compute_sudo=True, store=True, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    dias_laborables = fields.Integer(string='Dias', required=True,
                                     default=get_total_dias)
    cantidad_hombres = fields.Integer(string='Hombres', required=True)
    horas_laborables = fields.Integer(string='Horas',
                                      compute='_compute_horas_laborables',
                                      compute_sudo=True, store=True, )
    salario_directo = fields.Monetary(string='Salario directo',
                                      currency_field='company_currency_id',
                                      compute='_compute_salario_directo',
                                      compute_sudo=True, store=True, )
    estimulacion = fields.Monetary(string='Estimulación',
                                   currency_field='company_currency_id',
                                   compute='_compute_estimulacion',
                                   compute_sudo=True, store=True, )
    reserva_vacaciones = fields.Monetary(string='Reserva V.',
                                         currency_field='company_currency_id',
                                         compute='_compute_reserva_vacaciones',
                                         compute_sudo=True, store=True, )
    salario_total = fields.Monetary(string='Total',
                                    currency_field='company_currency_id',
                                    compute='_compute_salario_total',
                                    compute_sudo=True, store=True, )
    seguridad_social = fields.Monetary(string='Seguridad Social',
                                       currency_field='company_currency_id',
                                       compute='_compute_seguridad_social',
                                       compute_sudo=True, store=True, )
    gasto_directo = fields.Monetary(string='Gasto directo',
                                    currency_field='company_currency_id',
                                    compute='_compute_gasto_directo',
                                    compute_sudo=True, store=True, )
    gasto_indirecto = fields.Monetary(string='Gasto indirecto',
                                      currency_field='company_currency_id',
                                      compute='_compute_gasto_indirecto',
                                      compute_sudo=True, store=True, )
    presupuesto = fields.Monetary("Presupuesto",
                                  currency_field='company_currency_id',
                                  compute='_compute_presupuesto',
                                  compute_sudo=True, store=True, )
    presupuesto_dieta = fields.Monetary(
        "Presupuesto", compute='_compute_presupuesto_dieta',
        compute_sudo=True, store=True, currency_field='company_currency_id')
    alimentacion = fields.Monetary("Alimentación",
                                   currency_field='company_currency_id',
                                   compute='_compute_alimentacion',
                                   compute_sudo=True,
                                   store=True, )
    presupuesto_alimentacion = fields.Monetary(
        "Presupuesto", compute='_compute_presupuesto_alimentacion',
        compute_sudo=True, store=True, currency_field='company_currency_id')

    @api.depends('categoria_ocupacional_id')
    def _compute_alimentacion(self):
        for data in self:
            data.alimentacion = data.categoria_ocupacional_id.alimentacion

    # calculo el valor del presupuesto de la dieta
    @api.depends('dias_laborables', 'cantidad_hombres')
    def _compute_presupuesto_dieta(self):
        dieta = self.env['sicpro.nomenclador.dieta'].search(
            [('company_id', '=', self.company_id.id)], limit=1).name
        for data in self:
            data.presupuesto_dieta = data.dias_laborables * data.cantidad_hombres * dieta

    # calculo el valor del presupuesto de la alimentacion
    @api.depends('dias_laborables', 'cantidad_hombres')
    def _compute_presupuesto_alimentacion(self):
        for data in self:
            data.presupuesto_alimentacion = data.dias_laborables * data.cantidad_hombres * data.alimentacion

    # devuelve el valor del salario
    @api.depends('categoria_ocupacional_id')
    def _compute_salario(self):
        for data in self:
            data.salario = data.categoria_ocupacional_id.salario

    # devuelve el valor de la tarifa horaria
    @api.depends('categoria_ocupacional_id')
    def _compute_tarifa_horaria(self):
        tarifa = self.env['sicpro.nomenclador.tarifa.horaria'].search(
            [('company_id', '=', self.company_id.id)], limit=1)
        for data in self:
            data.tarifa_horaria = data.salario / tarifa.name

    # devuelve el valor de las horas laborables
    @api.depends('dias_laborables', 'cantidad_hombres')
    def _compute_horas_laborables(self):
        horas = self.env['resource.calendar'].search(
            [('company_id', '=', self.company_id.id)], limit=1).hours_per_day
        for data in self:
            data.horas_laborables = data.dias_laborables * horas * data.cantidad_hombres

    # devuelve el valor del salario directo a la producción
    @api.depends('tarifa_horaria', 'horas_laborables')
    def _compute_salario_directo(self):
        for data in self:
            data.salario_directo = data.tarifa_horaria * data.horas_laborables

    # devuelve el valor de la estimulacion
    @api.depends('salario_directo', )
    def _compute_estimulacion(self):
        estimulacion = self.env['sicpro.nomenclador.variables'].search(
            [('company_id', '=', self.company_id.id),
             ('name', '=', 'estimulacion')], limit=1).valor
        for data in self:
            data.estimulacion = data.salario_directo * estimulacion

    # devuelve el valor de la reserva de vacaciones
    @api.depends('salario_directo', 'estimulacion')
    def _compute_reserva_vacaciones(self):
        reserva = self.env['sicpro.nomenclador.variables'].search(
            [('company_id', '=', self.company_id.id),
             ('name', '=', 'vacaciones')], limit=1).valor
        for data in self:
            data.reserva_vacaciones = (
                                                  data.salario_directo + data.estimulacion) * reserva

    # devuelve el valor del salario total
    @api.depends('salario_directo', 'estimulacion', 'reserva_vacaciones')
    def _compute_salario_total(self):
        for data in self:
            data.salario_total = data.salario_directo + data.estimulacion + data.reserva_vacaciones

    # devuelve el valor de la seguridad social
    @api.depends('salario_total')
    def _compute_seguridad_social(self):
        social = self.env['sicpro.nomenclador.variables'].search(
            [('company_id', '=', self.company_id.id),
             ('name', '=', 'seguridad_social')], limit=1).valor
        for data in self:
            data.seguridad_social = data.salario_total * social

    # devuelve el valor de los gasto directo
    @api.depends('salario_total', 'seguridad_social')
    def _compute_gasto_directo(self):
        for data in self:
            data.gasto_directo = data.salario_total + data.seguridad_social

    # devuelve el valor de los gasto indirecto
    @api.depends('gasto_directo')
    def _compute_gasto_indirecto(self):
        indirectos = self.env['sicpro.nomenclador.variables'].search(
            [('company_id', '=', self.company_id.id),
             ('name', '=', 'gastos_indirectos')], limit=1).valor
        for data in self:
            data.gasto_indirecto = data.gasto_directo * indirectos

    # calculo el valor del presupuesto
    @api.depends('gasto_directo', 'gasto_indirecto')
    def _compute_presupuesto(self):
        for data in self:
            data.presupuesto = data.gasto_directo + data.gasto_indirecto
