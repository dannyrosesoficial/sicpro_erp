# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class SoporteCronogramaAnios(models.Model):
    _name = 'sicpro.app.soporte.cronograma.anio'
    _description = 'Años del Cronograma Planificado de Desarrollo'
    _order = "id"

    name = fields.Char(string='Año', required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    titulo = fields.Char(string='Titulo', compute='compute_titulo')
    user_id = fields.Many2one('res.users', index=True, default=lambda self: self.env.uid)

    @api.constrains('name')
    def _check_anio_unico(self):
        uniq = self.env['sicpro.app.soporte.cronograma.anio'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El año introducido existe!. Si cree que es un error contacte al administrador"))

    # genero el titulo del registro
    @api.depends('name')
    def compute_titulo(self):
        for item in self:
            item.titulo = 'Cronograma SICPRO ERP ' + str(item.name)

    # llamar al action para buscar las tareas del año del context
    def action_cronograma_plan(self):
        anio_activo = self._context.get('default_id')
        action = self.env['ir.actions.act_window']._for_xml_id('sicpro_app_soporte.soporte_cronograma_plan_action')
        action['domain'] = [('anio_id', '=', anio_activo), ('active', '=', True)]
        return action
