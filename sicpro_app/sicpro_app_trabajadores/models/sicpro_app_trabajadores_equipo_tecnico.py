# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class TrabajadoresEquipoTecnico(models.Model):
    _name = 'sicpro.app.trabajadores.equipo.tecnico'
    _description = 'Técnicos de los trabajadores'
    _order = "sequence"

    name = fields.Char(string='Equipo', required=True, )
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    lider = fields.Many2one("sicpro.app.trabajadores",
                            string="Lider de Equipo", required=True, )
    active = fields.Boolean(string='Activo', default=True, index=True)
    company_id = fields.Many2one('res.company', string='Proceso', index=True,
                                 default=lambda self: self.env.company)
    member_ids = fields.One2many('sicpro.app.trabajadores',
                                 'equipo_tecnico_id',
                                 string='Miembro del equipo', )
    areas_ids = fields.One2many('sicpro.app.trabajadores.areas',
                                'equipo_tecnico_id', string='Áreas', )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                   store=True,
                                   related='member_ids.ocupacion_id')
    movil_trabajo = fields.Char(string='movil_trabajo',
                                related='member_ids.movil_trabajo', store=True)
    correo_trabajo = fields.Char(string='correo_trabajo',
                                 related='member_ids.correo_trabajo',
                                 store=True)
    miembros_color = fields.Integer(string='miembros_color',
                                    related='member_ids.color', store=True)
    lider_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                         'lider_ocupacion_id', store=True,
                                         related='lider.ocupacion_id')
    lider_movil_trabajo = fields.Char(string='Móvil Trabajo', store=True,
                                      related='lider.movil_trabajo')
    lider_correo_trabajo = fields.Char(string='Correo Trabajo', store=True,
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
