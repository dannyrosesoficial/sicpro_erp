# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Departmentos(models.Model):
    _name = "sicpro.app.trabajadores.departmentos"
    _description = "Departamento de los trabajadores"
    _inherit = ['mail.thread']
    _order = "id"

    name = fields.Char('Departamento o Agrupación', required=True)
    complete_name = fields.Char('Complete Name',
                                compute='_compute_complete_name', store=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Proceso', index=True,
                                 default=lambda self: self.env.company)
    parent_id = fields.Many2one(
        'sicpro.app.trabajadores.departmentos',
        string='Departamento padre', index=True,
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id)]")
    child_ids = fields.One2many('sicpro.app.trabajadores.departmentos',
                                'parent_id', string='Departamento hijo')
    manager_id = fields.Many2one(
        'sicpro.app.trabajadores.general',
        string='Responsable', tracking=True,
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id)]")
    member_ids = fields.One2many('sicpro.app.trabajadores.general',
                                 'department_id', string='Miembros',
                                 readonly=True)
    jobs_ids = fields.One2many('sicpro.app.trabajadores.trabajos',
                               'department_id', string='Jobs')
    note = fields.Text('Note')
    color = fields.Integer('Color Index')
    centro_costo_usd = fields.Many2one(
        required=True, string='Centro Costo USD',
        comodel_name='sicpro.nomenclador.centro.costo')
    centro_costo_cup = fields.Char('Centro Costo CUP',
                                   required=True,
                                   related='centro_costo_usd.centro_costo_cup')
    local = fields.Many2many(
        'sicpro.nomenclador.locales', 'sicpro_app_trabajadores_departamentos_local_rel',
        'dpto_id', 'locales_id', string='local',
        domain="[('centro_costo_usd', '=', centro_costo_usd)]")
    tipo_registro = fields.Selection(
        string="", default='sin_categoría',
        selection=[('sin_categoría', 'Sin Categoría'),
                   ('departamento', 'Departamento'),
                   ('agrupacion', 'Agrupación'), ], )

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super(Departmentos, self).name_get()

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
                _('You cannot create recursive departments.'))

    @api.model
    def create(self, vals):
        # TDE note: auto-subscription of manager done by hand,because currently
        # the tracking allows to track+subscribe fields linked to a res.user
        # An update of the limited behavior should come, not currently done.
        department = super(Departmentos, self.with_context(
            mail_create_nosubscribe=True)).create(vals)
        manager = self.env['sicpro.app.trabajadores.general'].browse(
            vals.get("manager_id"))
        if manager.user_id:
            department.message_subscribe(
                partner_ids=manager.user_id.partner_id.ids)
        return department

    def write(self, vals):
        """ If updating manager of a department, we need to update all the
        employees of department hierarchy, and subscribe the new manager.
        """
        # TDE note: auto-subscription of manager done by hand,because currently
        # the tracking allows to track+subscribe fields linked to a res.user
        # An update of the limited behavior should come,but not currently done.
        if 'manager_id' in vals:
            manager_id = vals.get("manager_id")
            if manager_id:
                manager = self.env['sicpro.app.trabajadores.general'].browse(
                    manager_id)
                # subscribe the manager user
                if manager.user_id:
                    self.message_subscribe(
                        partner_ids=manager.user_id.partner_id.ids)
            # set the trabajadores parent to the new manager
            self._update_employee_manager(manager_id)
        return super(Departmentos, self).write(vals)

    def _update_employee_manager(self, manager_id):
        employees = self.env['sicpro.app.trabajadores.general']
        for department in self:
            employees = employees | self.env[
                'sicpro.app.trabajadores.general'].search([
                ('id', '!=', manager_id),
                ('department_id', '=', department.id),
                ('parent_id', '=', department.manager_id.id)])
        employees.write({'parent_id': manager_id})
