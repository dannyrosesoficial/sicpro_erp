# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MetrologiaCategoria(models.Model):
    _name = 'sicpro.app.metrologia.categoria'
    _inherit = ['mail.alias.mixin', 'mail.thread']
    _description = 'Categorías del Matenimiento de Equipos'

    @api.depends('equipment_ids')
    def _compute_fold(self):
        self.fold = False
        for category in self:
            category.fold = False if category.equipment_count else True

    name = fields.Char('Nombre', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    technician_user_id = fields.Many2one('res.users', 'Gestor de Equipos',
                                         tracking=True,
                                         default=lambda self: self.env.uid)
    color = fields.Integer('Color Index')
    note = fields.Text('Comentarios', translate=True)
    equipment_ids = fields.One2many('sicpro.app.metrologia.equipos',
                                    'category_id', string='Equipos',
                                    copy=False)
    equipment_count = fields.Integer(string="Equipos",
                                     compute='_compute_equipment_count')
    maintenance_ids = fields.One2many(
        'sicpro.app.metrologia.solicitud.calibracion', 'category_id',
        copy=False)
    maintenance_count = fields.Integer(string="Maintenance Count",
                                       compute='_compute_maintenance_count')
    alias_id = fields.Many2one(
        'mail.alias', 'Alias', ondelete='restrict', required=True,
        help="Email alias for this equipment category. "
             "New emails will automatically "
             "create a new equipment under this category.")
    fold = fields.Boolean(string='Folded in Maintenance Pipe',
                          compute='_compute_fold', store=True)

    def _compute_equipment_count(self):
        equipment_data = self.env['sicpro.app.metrologia.equipos'].read_group(
            [('category_id', 'in', self.ids)], ['category_id'],
            ['category_id'])
        mapped_data = dict([(m['category_id'][0],
                             m['category_id_count']) for m in equipment_data])
        for category in self:
            category.equipment_count = mapped_data.get(category.id, 0)

    def _compute_maintenance_count(self):
        maintenance_data = \
            self.env['sicpro.app.metrologia.solicitud.calibracion'].read_group(
                [('category_id', 'in', self.ids)],
                ['category_id'], ['category_id'])
        mapped_data = dict(
            [(m['category_id'][0], m['category_id_count']) for m in
             maintenance_data])
        for category in self:
            category.maintenance_count = mapped_data.get(category.id, 0)

    @api.model
    def create(self, vals):
        self = self.with_context(
            alias_model_name='sicpro.app.metrologia.solicitud.calibracion',
            alias_parent_model_name=self._name)
        if not vals.get('alias_name'):
            vals['alias_name'] = vals.get('name')
        category_id = super(MetrologiaCategoria, self).create(vals)
        category_id.alias_id.write(
            {'alias_parent_thread_id': category_id.id,
             'alias_defaults': {'category_id': category_id.id}})
        return category_id

    def unlink(self):
        MailAlias = self.env['mail.alias']
        for category in self:
            if category.equipment_ids or category.maintenance_ids:
                raise UserError(
                    _("You cannot delete an equipment category containing "
                      "equipments or maintenance requests."))
            MailAlias += category.alias_id
        res = super(MetrologiaCategoria, self).unlink()
        MailAlias.unlink()
        return res

    def get_alias_model_name(self, vals):
        return vals.get('alias_model',
                        'sicpro.app.metrologia.solicitud.calibracion')

    def get_alias_values(self):
        values = super(MetrologiaCategoria, self).get_alias_values()
        values['alias_defaults'] = {'category_id': self.id}
        return values
