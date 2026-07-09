# -*- coding: utf-8 -*-


from datetime import timedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PreparacionTecnicaActividades(models.Model):
    _name = "sicpro.app.preparacion.tecnica.actividades"
    _description = "Actividades de la Preparación Técnica"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']
    _order = "id asc"

    name = fields.Char("Actividad", index=True, required=True, tracking=True)
    especialidad = fields.Many2one("sicpro.nomenclador.especialidad",
                                   string="Especialidad",
                                   domain="[('company_id', '=', company_id)]",
                                   required=False, tracking=True)
    clasificacion = fields.Many2one(
        'sicpro.app.preparacion.tecnica.clasificacion',
        string="Clasificación", required=True,
        tracking=True)
    active = fields.Boolean(default=True)
    departamento = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                   string="Departamento", store=True,
                                   related='especialidad.departamento',
                                   readonly=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    descripcion = fields.Html(string='Descripción')
    color = fields.Integer(string='Color Index')
    favorito = fields.Boolean(string='Favorito')
    actividades_ids = fields.One2many(
        'sicpro.app.preparacion.tecnica.subactividades', 'actividad_id',
        string='Subactividades', )
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=False, )

    # redirección a la vista formulario de la actividad seleccionada
    def actividades_action(self):
        return {'name': 'Actividad',
                'view_mode': 'form',
                'res_model': 'sicpro.app.preparacion.tecnica.actividades',
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                }

    # cambio masivo de la clasificación de las subsolicitudes
    @api.onchange('clasificacion')
    def _onchange_clasificacion(self, ):
        data = self.env[
            'sicpro.app.preparacion.tecnica.subactividades'].search(
            [('actividad_id', '=', self._origin.id)])
        for items in data:
            items.clasificacion = self.clasificacion


class PreparacionTecnicaSubActividades(models.Model):
    _name = "sicpro.app.preparacion.tecnica.subactividades"
    _description = "Subactividades de la Preparación Técnica"
    _order = "id asc"

    name = fields.Char("Actividades", index=True, required=True, tracking=True)
    active = fields.Boolean(default=True)
    normas_tiempo = fields.Float(string='Normas de tiempo', required=True)
    tipo = fields.Char(string='Tipo', required=True, default="General")
    color = fields.Integer(string='Color Index')
    actividad_id = fields.Many2one(
        'sicpro.app.preparacion.tecnica.actividades', 'Actividad',
        index=True, )
    subactividad_id = fields.Many2one(
        'sicpro.app.preparacion.tecnica.subactividades', 'Actividades',
        index=True, copy=False, )
    especialidad = fields.Many2one("sicpro.nomenclador.especialidad",
                                   string="Especialidad")
    clasificacion = fields.Many2one(
        'sicpro.app.preparacion.tecnica.clasificacion',
        string="Clasificación", required=True, tracking=True)
    departamento = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                   string="Departamento", )
    company_id = fields.Many2one('res.company', string='Proceso')
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)

    @api.depends('name', 'tipo')
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.tipo:
                name = record.tipo + ' / ' + name
            res.append((record.id, name))
        return res


class PreparacionTecnicaActividadesForm(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.actividades.form'
    _description = 'Actividades del formulario de la Preparación Técnica'
    _order = "id asc"

    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=False, )
    subactividad_id = fields.Many2one(
        'sicpro.app.preparacion.tecnica.subactividades', 'Actividades',
        index=True, copy=False, )
    normas_tiempo = fields.Float(string='Norma',
                                 compute='_compute_normas_tiempo',
                                 store=True, readonly="True")
    tipo = fields.Char(string='Tipo', required=False)
    especialidad = fields.Many2one("sicpro.nomenclador.especialidad",
                                   string="Especialidad")
    clasificacion = fields.Many2one(
        'sicpro.app.preparacion.tecnica.clasificacion',
        string="Clasificación", required=True, tracking=True)
    departamento = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                   string="Departamento", )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    variable = fields.Integer(string='Variable', required=False)
    fecha_comienzo = fields.Date(string='Comienzo', required=True)
    fecha_terminacion = fields.Date(string='Terminación',
                                    compute='_compute_fecha_fin_actividades',
                                    store=True, readonly="True")

    # devuelve la norma de la actividad seleccionada
    @api.depends('subactividad_id.normas_tiempo', 'variable')
    def _compute_normas_tiempo(self):
        for data in self:
            if data.variable == 0:
                data.normas_tiempo = round(
                    sum(data.subactividad_id.mapped('normas_tiempo')),
                    2)
            else:
                data.normas_tiempo = round(
                    sum(data.subactividad_id.mapped('normas_tiempo')),
                    2) * data.variable

    # calcula la fecha final de cada actividad
    @api.depends('normas_tiempo')
    def _compute_fecha_fin_actividades(self):
        for data in self:
            horas = self.env['resource.calendar'].search(
                [('company_id', '=', self.company_id.id)],
                limit=1).hours_per_day
            dias = round(data.normas_tiempo, 2) / horas
            if data.fecha_comienzo:
                data.fecha_terminacion = data.fecha_comienzo + timedelta(
                    days=dias)

    @api.constrains("normas_tiempo")
    def _check_quantity(self):
        for actividad in self:
            if not actividad.normas_tiempo > 0.0:
                raise ValidationError(
                    _("Quantity of actividad consumed must be greater than 0.")
                )