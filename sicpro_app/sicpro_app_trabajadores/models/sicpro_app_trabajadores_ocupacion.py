# -*- coding: utf-8 -*-


from odoo import api, fields, models, _


class Trabajos(models.Model):
    _name = "sicpro.app.trabajadores.ocupacion"
    _description = "Categoría Ocupacional del trabajador"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'area_sequence, id'

    name = fields.Many2one(comodel_name='sicpro.app.trabajadores.cargos', string='Categoría Ocupacional', required=True)
    active = fields.Boolean(string="Activo", default=True, )
    cantidad_trabajadores = fields.Integer(compute='_compute_cuenta_trabajadores', string="Cantidad de trabajadores",
                                           store=True, )
    descripcion = fields.Text(string='Descripción del trabajo')
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', string='Departamento', required=True, )
    area_sequence = fields.Integer(related='area_id.departamento_sequence', store=True)
    company_id = fields.Many2one('res.company', string='Proceso', readonly=True, store=True,
                                 related='area_id.company_id', )
    company_currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id',
                                          readonly=True)
    trabajadores_ids = fields.One2many('sicpro.app.trabajadores', 'ocupacion_id', string='Trabajadores', )
    salario = fields.Monetary("Salario", currency_field='company_currency_id', related='name.salario', store=True, )
    alimentacion = fields.Monetary("Alimentación", currency_field='company_currency_id', related='name.alimentacion',
                                   store=True, )

    _sql_constraints = [('name_uniq', 'unique(name, company_id, area_id)',
                         'Ya existe ese puesto de trabajo para el departamento del proceso específico'), ]

    # Cuenta la cantidad de trabajadores existentes en la categoría
    @api.depends('trabajadores_ids.ocupacion_id', 'trabajadores_ids.active')
    def _compute_cuenta_trabajadores(self):
        trabajadores_data = self.env['sicpro.app.trabajadores'].read_group([('ocupacion_id', 'in', self.ids)],
            ['ocupacion_id'], ['ocupacion_id'])
        result = dict((data['ocupacion_id'][0], data['ocupacion_id_count']) for data in trabajadores_data)
        for ocupacion in self:
            ocupacion.cantidad_trabajadores = result.get(ocupacion.id, 0)

    @api.model
    def create(self, values):
        return super(Trabajos, self.with_context(mail_create_nosubscribe=True)).create(values)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % self.name
        return super(Trabajos, self).copy(default=default)
