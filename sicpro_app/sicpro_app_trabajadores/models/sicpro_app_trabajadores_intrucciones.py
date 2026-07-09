# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrabajadoresIntrucciones(models.Model):
    _name = 'sicpro.app.trabajadores.intrucciones'
    _description = 'Instrucciones de los trabajadores'
    _order = "fecha_desde asc"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    plaza_id = fields.Char(string="# Plaza", required=True)
    name = fields.Many2one('sicpro.app.trabajadores', required=False, )
    instructor_plaza = fields.Char(string="Plaza Instructor", required=False)
    instructor = fields.Many2one('sicpro.app.trabajadores', string="Instructor", required=False, )
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo',
                                   related='instructor.ocupacion_id')
    tipo_intruccion = fields.Char(string='Tipo de Instrucción', required=False)
    fecha_desde = fields.Date(string='Desde', required=False)
    evalucion = fields.Integer(string='Evaluación', required=False)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    @api.model
    def create(self, vals):
        instruciones = super(TrabajadoresIntrucciones, self).create(vals)
        trabajador = self.env['sicpro.app.trabajadores'].search([('plaza_id', '=', vals.get('plaza_id')), ])
        instructor = self.env['sicpro.app.trabajadores'].search([('plaza_id', '=', vals.get('instructor_plaza')), ])
        instruciones['name'] = trabajador.id
        instruciones['instructor'] = instructor.id
        return instruciones
