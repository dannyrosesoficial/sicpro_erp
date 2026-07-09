# -*- coding: utf-8 -*-
import logging
from odoo.addons.survey.controllers.main import Survey
from odoo import http, SUPERUSER_ID
from odoo.http import request, content_disposition
from odoo.osv import expression
_logger = logging.getLogger(__name__)

class Encuestas(Survey):

    @http.route('/survey/results/<model("survey.survey"):survey>', type='http', auth='user', website=True)
    def survey_report(self, survey, answer_token=None, **post):
        user_input_lines, search_filters = self._extract_filters_data(survey, post)
        survey_data = survey._prepare_statistics(user_input_lines)
        question_and_page_data = survey.question_and_page_ids._prepare_statistics(user_input_lines)
        template_values = {
            'survey': survey,
            'question_and_page_data': question_and_page_data,
            'survey_data': survey_data,
            'search_filters': search_filters,
            'search_finished': post.get('finished') == 'true',
        }
        if survey.session_show_leaderboard:
            template_values['leaderboard'] = survey._prepare_leaderboard_values()
        return request.render('survey.survey_page_statistics', template_values)

    def _get_user_input_domain(self, survey, line_filter_domain, **post):
        user_input_domain = ['&', ('test_entry', '=', False), ('survey_id', '=', survey.id)]
        if line_filter_domain:
            matching_line_ids = request.env['survey.user_input.line'].sudo().search(line_filter_domain).ids
            user_input_domain = expression.AND([
                [('user_input_line_ids', 'in', matching_line_ids)],
                user_input_domain
            ])
        if post.get('finished'):
            user_input_domain = expression.AND([[('state', '=', 'done')], user_input_domain])
        else:
            user_input_domain = expression.AND([[('state', '!=', 'new')], user_input_domain])
        return user_input_domain

    def _extract_filters_data(self, survey, post):
        search_filters = []
        line_filter_domain = []
        line_choices = []
        raw_filters = post.get('filters', '') or ''
        for data in raw_filters.split('|'):
            data = data.strip()
            if not data:
                continue
            try:
                parts = [int(x) for x in data.split(',') if x.strip()]
            except ValueError:
                _logger.warning("Malformed filter ignored: %s", data)
                continue
            if len(parts) == 2:
                row_id, answer_id = parts
                if row_id and answer_id:
                    line_filter_domain = expression.AND([
                        ['&', ('matrix_row_id', '=', row_id), ('suggested_answer_id', '=', answer_id)],
                        line_filter_domain
                    ])
                    ans_row = request.env['survey.question.answer'].sudo().browse(row_id)
                    ans_answer = request.env['survey.question.answer'].sudo().browse(answer_id)
                    if not ans_row or not ans_answer:
                        _logger.warning("Filter references non-existing answer ids: %s", parts)
                        continue
                    question_id = ans_row.matrix_question_id or ans_row.question_id
                    search_filters.append({
                        'question': question_id.title,
                        'answers': '%s: %s' % (ans_row.value or '', ans_answer.value or '')
                    })
            elif len(parts) == 1:
                answer_id = parts[0]
                if answer_id:
                    line_choices.append(answer_id)
                    ans = request.env['survey.question.answer'].sudo().browse(answer_id)
                    if not ans:
                        _logger.warning("Filter references non-existing answer id: %s", answer_id)
                        continue
                    question_id = ans.matrix_question_id or ans.question_id
                    search_filters.append({
                        'question': question_id.title,
                        'answers': ans.value or ''
                    })
        if line_choices:
            line_filter_domain = expression.AND([[('suggested_answer_id', 'in', line_choices)], line_filter_domain])
        user_input_domain = self._get_user_input_domain(survey, line_filter_domain, **post)
        user_input_lines = request.env['survey.user_input'].sudo().search(user_input_domain).mapped('user_input_line_ids')
        return user_input_lines, search_filters
