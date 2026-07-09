# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class TrabajadoresEquipoTecnico(models.Model):
    _name = 'sicpro.app.trabajadores.equipo.tecnico'
    _description = 'Técnicos de los trabajadores'
    _order = "sequence"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char('Equipo', required=True, )
    sequence = fields.Integer('Sequence', default=10)
    lider = fields.Many2one("sicpro.app.trabajadores", string="Lider de Equipo", required=True, )
    active = fields.Boolean(default=True, )
    company_id = fields.Many2one('res.company', string='Proceso', index=True, default=lambda self: self.env.company)
    member_ids = fields.One2many('sicpro.app.trabajadores', 'equipo_tecnico_id', string='Miembro del equipo', )
    areas_ids = fields.One2many('sicpro.app.trabajadores.areas', 'equipo_tecnico_id', string='Áreas', )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', store=True, related='member_ids.ocupacion_id')
    movil_trabajo = fields.Char('movil_trabajo', related='member_ids.movil_trabajo', store=True)
    correo_trabajo = fields.Char('correo_trabajo', related='member_ids.correo_trabajo', store=True)
    miembros_color = fields.Integer('miembros_color', related='member_ids.color', store=True)
    lider_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'lider_ocupacion_id', store=True,
                                         related='lider.ocupacion_id')
    lider_movil_trabajo = fields.Char('Móvil Trabajo', store=True, related='lider.movil_trabajo')
    lider_correo_trabajo = fields.Char('Correo Trabajo', store=True, related='lider.correo_trabajo')
    trabajadores_count = fields.Integer(compute='_trabajadores_count', string='Cantidad Trabajadores')
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP', store=True, related='lider.user_id')
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    # Cuenta la cantidad de trabajadores del proceso
    def _trabajadores_count(self):
        model_trabajadores = self.env['sicpro.app.trabajadores']
        for trabajadores in self:
            trabajadores.trabajadores_count = model_trabajadores.search_count(
                [('area_id', 'in', trabajadores.areas_ids.ids)])
