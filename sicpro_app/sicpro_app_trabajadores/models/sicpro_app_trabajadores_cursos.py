# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TrabajadoresCursos(models.Model):
    _name = 'sicpro.app.trabajadores.cursos'
    _description = 'Cursos de los trabajadores'
    _rec_name = 'skill_id'
    _order = "skill_level_id"

    employee_id = fields.Many2one('sicpro.app.trabajadores', required=True, ondelete='cascade')
    skill_id = fields.Many2one('sicpro.app.trabajadores.cursos.habilidades', string='Habilidades', required=True)
    skill_level_id = fields.Many2one('sicpro.app.trabajadores.cursos.niveles', string='Nivel de Habilidad',
                                     required=True)
    skill_type_id = fields.Many2one('sicpro.app.trabajadores.cursos.tipos', string='Cursos', required=True)
    level_progress = fields.Integer(related='skill_level_id.level_progress')

    _sql_constraints = [
        ('_unique_skill', 'unique (employee_id, skill_id)', "No se permiten dos niveles para la misma habilidad"), ]

    @api.constrains('skill_id', 'skill_type_id')
    def _check_skill_type(self):
        for record in self:
            if record.skill_id not in record.skill_type_id.skill_ids:
                raise ValidationError(
                    _("La habilidad %(name)s y tipo de habilidad %(type)s no coincide", name=record.skill_id.name,
                      type=record.skill_type_id.name))

    @api.constrains('skill_type_id', 'skill_level_id')
    def _check_skill_level(self):
        for record in self:
            if record.skill_level_id not in record.skill_type_id.skill_level_ids:
                raise ValidationError(
                    _("El nivel de habilidad %(level)s no es válido para el tipo de habilidad: %(type)s",
                      level=record.skill_level_id.name, type=record.skill_type_id.name))
