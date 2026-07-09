# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from random import randint


class Team(models.Model):
    _name = 'sicpro.app.trabajadores.equipo.tecnico'
    _description = 'Técnicos de los trabajadores'
    _order = "sequence"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Equipo', required=True, )
    sequence = fields.Integer('Sequence', default=10)
    lider = fields.Many2one("sicpro.app.trabajadores",
                            string="Lider de Equipo", required=True,)
    active = fields.Boolean(default=True, )
    company_id = fields.Many2one('res.company', string='Proceso', index=True,
                                 default=lambda self: self.env.company)
    member_ids = fields.One2many('sicpro.app.trabajadores',
                                 'equipo_tecnico_id',
                                 string='Miembro del equipo', )
    areas_ids = fields.One2many('sicpro.app.trabajadores.areas',
                                 'equipo_tecnico_id', string='Áreas', )


    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                   store=True,
                                   related='member_ids.ocupacion_id')
    movil_trabajo = fields.Char('movil_trabajo',
                                related='member_ids.movil_trabajo', store=True)
    correo_trabajo = fields.Char('correo_trabajo',
                                 related='member_ids.correo_trabajo',
                                 store=True)
    miembros_color = fields.Integer('miembros_color',
                                    related='member_ids.color', store=True)
    lider_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                         'lider_ocupacion_id', store=True,
                                         related='lider.ocupacion_id')
    lider_movil_trabajo = fields.Char('Móvil Trabajo', store=True,
                                related='lider.movil_trabajo')
    lider_correo_trabajo = fields.Char('Correo Trabajo', store=True,
                                 related='lider.correo_trabajo')
    trabajadores_count = fields.Integer(compute='_trabajadores_count',
                                        string='Cantidad Trabajadores')
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP', store=True,
                              related='lider.user_id')

    # Cuenta la cantidad de trabajadores del proceso
    def _trabajadores_count(self):
        model_trabajadores = self.env['sicpro.app.trabajadores']
        for trabajadores in self:
            trabajadores.trabajadores_count = model_trabajadores.search_count(
                [('area_id', 'in', trabajadores.areas_ids.ids)])
