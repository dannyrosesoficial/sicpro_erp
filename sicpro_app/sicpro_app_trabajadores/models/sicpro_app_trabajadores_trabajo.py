# -*- coding: utf-8 -*-


from odoo import api, fields, models, _


class Trabajos(models.Model):
    _name = "sicpro.app.trabajadores.trabajos"
    _description = "Categoría Ocupacional"
    _inherit = ['mail.thread']

    name = fields.Many2one(
        comodel_name='sicpro.nomenclador.categoria.ocupacional',
        string='Categoría Ocupacional', required=True)
    active = fields.Boolean(string="Activo", default=True, )
    cantidad_trabajadores = fields.Integer(
        compute='_compute_cuenta_trabajadores',
        string="Número actual de trabajadores",
        store=True,
        help='Number of employees currently occupying this job position.')
    descripcion = fields.Text(string='Descripción del trabajo')
    department_id = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                    string='Departamento', required=True,
                                    domain="['|', ('company_id', '=', False), "
                                           "('company_id', '=', company_id)]")
    company_id = fields.Many2one('res.company', string='Proceso',
                                 readonly=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    trabajadores_ids = fields.One2many('sicpro.app.trabajadores.general',
                                       'job_id',
                                       string='Trabajadores', )
    salario = fields.Monetary("Salario", currency_field='company_currency_id',
                              compute='_compute_salario', compute_sudo=True,
                              store=True, )
    alimentacion = fields.Monetary("Alimentación",
                                   currency_field='company_currency_id',
                                   compute='_compute_alimentacion',
                                   compute_sudo=True,
                                   store=True, )

    _sql_constraints = [
        ('name_uniq', 'unique(name, company_id, department_id)',
         'Ya existe ese puesto de trabajo para el departamento del proceso especifico'),
    ]

    # Cuenta la cantidad de trabajadores existentes en la categoría
    @api.depends('trabajadores_ids.job_id', 'trabajadores_ids.active')
    def _compute_cuenta_trabajadores(self):
        employee_data = self.env['sicpro.app.trabajadores.general'].read_group(
            [('job_id', 'in', self.ids)], ['job_id'], ['job_id'])
        result = dict((data['job_id'][0], data['job_id_count'])
                      for data in employee_data)
        for job in self:
            job.cantidad_trabajadores = result.get(job.id, 0)

    # busca el valor del salario de la categoría
    @api.depends('name')
    def _compute_salario(self):
        for data in self:
            data.salario = data.name.salario

    # busca el valor de la alimentación de la categoría
    @api.depends('name')
    def _compute_alimentacion(self):
        for data in self:
            data.alimentacion = data.name.alimentacion

    @api.model
    def create(self, values):
        """ We don't want the current user to be follower of all
         created job """
        return super(Trabajos, self.with_context(
            mail_create_nosubscribe=True)).create(values)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        return super(Trabajos, self).copy(default=default)
