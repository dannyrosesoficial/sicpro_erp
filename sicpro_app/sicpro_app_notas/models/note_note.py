# -*- coding: utf-8 -*-


from random import randint

from odoo import api, fields, models


def _default_color():
    return randint(1, 11)


class Note(models.Model):
    _inherit = 'note.note'

    def _get_default_stage_id(self):
        tablero_activo = self._context.get('default_id')
        return self.env['note.stage'].search([
            ('user_id', '=', self.env.uid), ('tableros_id', '=', tablero_activo)], limit=1)

    tableros_id = fields.Many2one('note.tableros', string='Tableros', required=True)

    def _compute_stage_id(self):
        tablero_activo = self._context.get('default_id')
        first_user_stage = self.env['note.stage'].search([
            ('user_id', '=', self.env.uid), ('tableros_id', '=', tablero_activo)], limit=1)
        for note in self:
            for stage in note.stage_ids.filtered(lambda stage: stage.user_id == self.env.user):
                note.stage_id = stage
            # note without user's stage
            if not note.stage_id:
                note.stage_id = first_user_stage

    def _inverse_stage_id(self):
        for note in self.filtered('stage_id'):
            note.stage_ids = note.stage_id + note.stage_ids.filtered(
                lambda stage: stage.user_id != self.env.user and stage.tableros_id == self._context.get('default_id'))

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if groupby and groupby[0] == "stage_id" and (len(groupby) == 1 or lazy):
            tablero_activo = self._context.get('default_id')
            stages = self.env['note.stage'].search([
                ('user_id', '=', self.env.uid), ('tableros_id', '=', tablero_activo)])
            if stages:  # if the user has some stages
                result = [{  # notes by stage for stages user
                    '__context': {'group_by': groupby[1:]},
                    '__domain': domain + [('stage_ids.id', '=', stage.id)],
                    'stage_id': (stage.id, stage.name),
                    'stage_id_count': self.search_count(domain + [('stage_ids', '=', stage.id)]),
                    '__fold': stage.fold,
                } for stage in stages]

                # note without user's stage
                nb_notes_ws = self.search_count(domain + [('stage_ids', 'not in', stages.ids)])
                if nb_notes_ws:
                    # add note to the first column if it's the first stage
                    dom_not_in = ('stage_ids', 'not in', stages.ids)
                    if result and result[0]['stage_id'][0] == stages[0].id:
                        dom_in = result[0]['__domain'].pop()
                        result[0]['__domain'] = domain + ['|', dom_in, dom_not_in]
                        result[0]['stage_id_count'] += nb_notes_ws
                    else:
                        # add the first stage column
                        result = [{
                            '__context': {'group_by': groupby[1:]},
                            '__domain': domain + [dom_not_in],
                            'stage_id': (stages[0].id, stages[0].name),
                            'stage_id_count': nb_notes_ws,
                            '__fold': stages[0].name,
                        }] + result
            else:  # if stage_ids is empty, get note without user's stage
                nb_notes_ws = self.search_count(domain)
                if nb_notes_ws:
                    result = [{  # notes for unknown stage
                        '__context': {'group_by': groupby[1:]},
                        '__domain': domain,
                        'stage_id': False,
                        'stage_id_count': nb_notes_ws
                    }]
                else:
                    result = []
            return result
        return super(Note, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

