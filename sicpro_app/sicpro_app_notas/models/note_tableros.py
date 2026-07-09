# -*- coding: utf-8 -*-


from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class Tableros(models.Model):
    _name = "note.tableros"
    _description = "Tableros de Notas"
    _order = 'sequence'

    name = fields.Char('Tablero', required=True)
    sequence = fields.Integer(default=1)
    user_id = fields.Many2one('res.users', string='Usuario', required=True, ondelete='cascade',
                              default=lambda self: self.env.uid,)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    # llamar al action para buscar las tareas del tablero del context
    def action_tablero(self):
        tablero_activo = self._context.get('default_id')
        action = self.env['ir.actions.act_window']._for_xml_id('note.action_note_note')
        action['domain'] = [('tableros_id', '=', tablero_activo)]
        return action


