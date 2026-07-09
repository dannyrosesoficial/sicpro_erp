# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class TrabajadoresCursos(models.Model):
    _name = 'sicpro.app.trabajadores.cursos'
    _description = 'Cursos de los trabajadores'
    _rec_name = 'skill_id'
    _order = "skill_level_id"

    employee_id = fields.Many2one('sicpro.app.trabajadores', required=True,
                                  ondelete='cascade')
    skill_id = fields.Many2one('sicpro.app.trabajadores.cursos.habilidades',
                               string='Habilidades', required=True)
    skill_level_id = fields.Many2one('sicpro.app.trabajadores.cursos.niveles',
                                     string='Nivel de Habilidad',
                                     required=True)
    skill_type_id = fields.Many2one('sicpro.app.trabajadores.cursos.tipos',
                                    string='Cursos', required=True)
    level_progress = fields.Integer(related='skill_level_id.level_progress')

    @api.constrains('employee_id', 'skill_id')
    def _check_unique_employee_skill(self):
        for record in self:
            # Buscamos si ya existe la combinación Empleado + Habilidad
            domain = [('employee_id', '=', record.employee_id.id),
                ('skill_id', '=', record.skill_id.id), ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡Error de Competencias! El empleado '%s' ya tiene registrada la habilidad '%s'. "
                    "No se permiten asignar dos niveles o duplicar la misma habilidad para un mismo trabajador." % (
                    record.employee_id.name,
                    record.skill_id.name) + MSG_SOPORTE_SICPRO)

    @api.constrains('skill_id', 'skill_type_id')
    def _check_skill_type(self):
        for record in self:
            if record.skill_id not in record.skill_type_id.skill_ids:
                raise ValidationError(
                    f"La habilidad {record.skill_id.name} y el tipo de habilidad {record.skill_type_id.name} no coinciden.\n\n" + MSG_SOPORTE_SICPRO)

    @api.constrains('skill_type_id', 'skill_level_id')
    def _check_skill_level(self):
        for record in self:
            if record.skill_level_id not in record.skill_type_id.skill_level_ids:
                raise ValidationError(
                    f"El nivel de habilidad {record.skill_level_id.name} no es válido para el tipo de habilidad: {record.skill_type_id.name}.\n\n" + MSG_SOPORTE_SICPRO)
