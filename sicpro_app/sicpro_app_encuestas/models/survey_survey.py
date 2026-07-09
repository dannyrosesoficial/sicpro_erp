# -*- coding: utf-8 -*-

import json

from odoo import models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    # ------------------------------------------------------------
    # GRAPH / RESULTS
    # ------------------------------------------------------------

    def _prepare_statistics(self, user_input_lines=None):
        if user_input_lines:
            user_input_domain = [('survey_id', 'in', self.ids),
                                 ('id', 'in', user_input_lines.mapped('user_input_id').ids)]
        else:
            user_input_domain = [('survey_id', 'in', self.ids), ('state', '=', 'done'), ('test_entry', '=', False)]
        count_data = self.env['survey.user_input'].sudo().read_group(user_input_domain,
                                                                     ['scoring_success', 'id:count_distinct'],
                                                                     ['scoring_success'])

        scoring_success_count = 0
        scoring_failed_count = 0
        for count_data_item in count_data:
            if count_data_item['scoring_success']:
                scoring_success_count += count_data_item['scoring_success_count']
            else:
                scoring_failed_count += count_data_item['scoring_success_count']

        success_graph = json.dumps([{'text': _('Passed'), 'count': scoring_success_count, 'color': '#2E7D32'},
                                    {'text': _('Missed'), 'count': scoring_failed_count, 'color': '#C62828'}])

        total = scoring_success_count + scoring_failed_count
        return {'global_success_rate': round((scoring_success_count / total) * 100, 1) if total > 0 else 0,
                'global_success_graph': success_graph}
