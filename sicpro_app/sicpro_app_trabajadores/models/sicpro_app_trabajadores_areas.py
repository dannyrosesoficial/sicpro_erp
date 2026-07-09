# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class TrabajadoresDepartamentos(models.Model):
    _name = "sicpro.app.trabajadores.areas"
    _description = "Departamento de los trabajadores"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'departamento_sequence, id'

    name = fields.Char(string='Área', index=True,
                       compute='_compute_departamento_name', store=True)
    departamento_ids = fields.Many2one('sicpro.nomenclador.departamentos',
                                       string='Áreas', required=True,
                                       domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    departamento_sequence = fields.Integer(related='departamento_ids.sequence',
                                           store=True)
    complete_name = fields.Char(string='Complete Name', recursive=True,
                                compute='_compute_complete_name', store=True)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Proceso', index=True,
                                 required=True, )
    parent_id = fields.Many2one('sicpro.app.trabajadores.areas',
                                string='Departamento padre', index=True,
                                domain="['|', ('company_id', '=', False),  ('company_id', '=', company_id)]")
    child_ids = fields.One2many('sicpro.app.trabajadores.areas', 'parent_id',
                                string='Departamento hijo')
    manager_id = fields.Many2one('sicpro.app.trabajadores',
                                 string='Responsable', tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    manager_id_hide = fields.Many2one('sicpro.app.trabajadores',
                                      string='Responsable.', tracking=True,
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    member_ids = fields.One2many('sicpro.app.trabajadores', 'area_id',
                                 string='Miembros', readonly=True)
    jobs_ids = fields.One2many('sicpro.app.trabajadores.ocupacion', 'area_id',
                               string='Jobs')
    note = fields.Text(string='Note')
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    centro_costo = fields.Many2one(required=True, string='Centro Costo',
                                   comodel_name='sicpro.nomenclador.centro.costo',
                                   domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    local = fields.Many2many('sicpro.nomenclador.locales',
                             'sicpro_app_trabajadores_departamentos_local_rel',
                             'dpto_id', 'locales_id', string='local',
                             domain="[('centro_costo', '=', centro_costo)]")
    tipo_registro = fields.Selection(string="", default='sin_categoría',
                                     selection=[('sin_categoría', 'Dirección'),
                                                ('departamento',
                                                 'Departamento/Grupo'), (
                                                'agrupacion',
                                                'Agrupación'), ], )
    equipo_tecnico_id = fields.Many2one(
        "sicpro.app.trabajadores.equipo.tecnico", string="Equipo Técnico")

    # actualizar el trabajador y el usuario si es jefe
    @api.onchange('manager_id')
    def _onchange_manager_id(self):
        if self.manager_id:
            self.manager_id_hide = self.manager_id
        else:
            self.manager_id_hide = None

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super(TrabajadoresDepartamentos, self).name_get()

    @api.depends('departamento_ids')
    def _compute_departamento_name(self):
        self.name = self.departamento_ids.name

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s / %s' % (
                department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(
                'No se pueden crear departamentos duplicados.' + MSG_SOPORTE_SICPRO)

    @api.model_create_multi
    def create(self, vals_list):
        departments = super(TrabajadoresDepartamentos, self.with_context(
            mail_create_nosubscribe=True)).create(vals_list)

        # 2. Iteramos sobre los registros creados y sus valores correspondientes
        for department, vals in zip(departments, vals_list):
            manager_id = vals.get("manager_id")
            if manager_id:
                # Buscamos el manager en el modelo de trabajadores de SICPRO
                manager = self.env['sicpro.app.trabajadores'].browse(
                    manager_id)

                # Verificamos que tenga usuario y partner para evitar errores de None
                if manager.user_id and manager.user_id.partner_id:
                    department.message_subscribe(
                        partner_ids=manager.user_id.partner_id.ids)

        return departments

    def write(self, vals):
        if 'manager_id' in vals:
            manager_id = vals.get("manager_id")
            if manager_id:
                manager = self.env['sicpro.app.trabajadores'].browse(
                    manager_id)
                # subscribe the manager user
                if manager.user_id:
                    self.message_subscribe(
                        partner_ids=manager.user_id.partner_id.ids)
            self._update_employee_manager(manager_id)
        return super(TrabajadoresDepartamentos, self).write(vals)

    def _update_employee_manager(self, manager_id):
        employees = self.env['sicpro.app.trabajadores']
        for department in self:
            employees = employees | self.env['sicpro.app.trabajadores'].search(
                [('id', '!=', manager_id), ('area_id', '=', department.id),
                 ('parent_id', '=', department.manager_id.id)])
        employees.write({'parent_id': manager_id})
