# -*- coding: utf-8 -*-
from odoo import api, fields, models
import json
from collections import Counter

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    @api.model
    def _prepare_statistics(self, user_input_lines=None):
        results = []
        for question in self:
            if user_input_lines:
                q_lines = user_input_lines.filtered(lambda l: l.question_id.id == question.id)
            else:
                q_lines = self.env['survey.user_input.line'].sudo().search([('question_id','=',question.id),('skipped','=',False)])

            done = q_lines.filtered(lambda l: not l.skipped)
            skipped = q_lines.filtered(lambda l: l.skipped)
            comment_lines = q_lines.filtered(lambda l: l.answer_type in ['char_box','text_box'] and l.value_text_box)

            data = {'question': question,
                    'answer_input_done_ids': done,
                    'answer_input_skipped_ids': skipped,
                    'comment_line_ids': comment_lines,
                    'graph_data': None,
                    'table_data': [],
                    'right_answers': [],
                    'right_inputs_count': 0,
                    'partial_inputs_count': 0}

            qtype = question.question_type

            if qtype in ['text_box','char_box','datetime','time','date','month','url','email','password']:
                data['table_data'] = list(done)

            elif qtype == 'selection':
                vals = [ (l.value_selection or '') for l in done ]
                counts = Counter(vals)
                data['table_data'] = [{'value':v,'count':c,'suggested_answer':False} for v,c in counts.items()]
                data['graph_data'] = [{'text':v,'count':c} for v,c in counts.items()]

            elif qtype == 'many2one':
                vals = [ (l.value_many2one_option or '') for l in done ]
                counts = Counter(vals)
                data['table_data'] = [{'value':v,'count':c,'suggested_answer':False} for v,c in counts.items()]
                data['graph_data'] = [{'text':v,'count':c} for v,c in counts.items()]

            elif qtype == 'many2many':
                all_items = []
                for l in done:
                    try:
                        items = json.loads(l.value_many2many) if l.value_many2many else []
                    except Exception:
                        items = []
                    if isinstance(items, (list,tuple)):
                        all_items += items
                counts = Counter(all_items)
                data['table_data'] = [{'value':v,'count':c,'suggested_answer':False} for v,c in counts.items()]
                data['graph_data'] = [{'text':v,'count':c} for v,c in counts.items()]

            elif qtype == 'range':
                nums = []
                for l in done:
                    try:
                        nums.append(float(l.value_range))
                    except Exception:
                        pass
                if nums:
                    data['numerical_min'] = min(nums)
                    data['numerical_max'] = max(nums)
                    data['numerical_average'] = sum(nums)/len(nums)
                data['table_data'] = [{'value':v,'count':1} for v in nums]

            elif qtype in ['barcode','qr','name','address','color','week']:
                data['table_data'] = list(done)

            elif qtype == 'matrix' and question.matrix_subtype == 'custom':
                data['table_data'] = list(done)

            if qtype == 'time':
                buckets = Counter()
                for l in done:
                    val = l.value_time or ''
                    if val:
                        try:
                            hour = int(str(val).split(':')[0])
                        except Exception:
                            hour = None
                        if hour is not None:
                            buckets[f"{hour}:00"] += 1
                data['graph_data'] = [{'text':k,'count':v} for k,v in buckets.items()] if buckets else data['graph_data']

            if qtype == 'month':
                buckets = Counter()
                for l in done:
                    val = l.value_month or ''
                    if val:
                        buckets[val] += 1
                data['graph_data'] = [{'text':k,'count':v} for k,v in buckets.items()] if buckets else data['graph_data']

            if qtype == 'week':
                buckets = Counter()
                for l in done:
                    val = l.value_week or ''
                    if val:
                        buckets[val] += 1
                data['graph_data'] = [{'text':k,'count':v} for k,v in buckets.items()] if buckets else data['graph_data']

            results.append(data)
        return results
