# -*- coding: utf-8 -*-
import json
from odoo import api, fields, models

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def save_lines(self, question, answer, comment=None):
        old_answers = self.env['survey.user_input.line'].search([('user_input_id','=',self.id),('question_id','=',question.id)])
        if question.question_type in ['password','range','time','url','email','many2many','file','many2one','week','color','month','address','name','selection','qr','barcode'] or question.matrix_subtype == 'custom':
            return self._save_user_answers(question, old_answers, answer)
        return super().save_lines(question, answer, comment)

    def _save_user_answers(self, question, user_input_line, answer):
        vals = self._get_user_answers(question, answer, question.question_type)
        if user_input_line:
            user_input_line.write(vals)
            return user_input_line
        return self.env['survey.user_input.line'].create(vals)

    def _get_user_answers(self, question, answer, answer_type):
        vals = {'user_input_id': self.id, 'question_id': question.id, 'skipped': False, 'answer_type': answer_type}
        if not answer or (isinstance(answer, str) and not answer.strip()):
            vals.update(answer_type=None, skipped=True)
            return vals
        if question.question_type == 'time':
            vals['value_time'] = answer if isinstance(answer, str) else str(answer)
        elif question.question_type == 'url':
            vals['value_url'] = answer
        elif question.question_type == 'password':
            vals['value_password'] = answer
        elif question.question_type == 'email':
            vals['value_email'] = answer
        elif question.question_type == 'range':
            vals['value_range'] = str(answer)
        elif question.question_type == 'many2one':
            if isinstance(answer, (list,tuple)) and len(answer)>=2:
                vals['value_many2one'] = str(answer[0])
                vals['value_many2one_option'] = str(answer[1])
            else:
                vals['value_many2one'] = str(answer)
                vals['value_many2one_option'] = ''
        elif question.question_type == 'many2many':
            vals['value_many2many'] = json.dumps(answer)
        elif question.question_type == 'week':
            vals['value_week'] = answer
        elif question.question_type == 'color':
            vals['value_color'] = answer
        elif question.question_type == 'date':
            vals['value_date'] = answer
        elif question.question_type == 'month':
            vals['value_month'] = answer
        elif question.question_type == 'matrix' and question.matrix_subtype == 'custom':
            vals['value_matrix'] = json.dumps(answer)
        elif question.question_type == 'address':
            vals['value_address'] = json.dumps(answer)
        elif question.question_type == 'qr':
            vals['value_qr'] = json.dumps(answer)
        elif question.question_type == 'barcode':
            vals['value_barcode'] = json.dumps(answer)
        elif question.question_type == 'name':
            vals['value_name'] = json.dumps(answer)
        elif question.question_type == 'selection':
            vals['value_selection'] = answer
        elif question.question_type == 'file':
            attachment = self.env['ir.attachment'].create({'name': str(answer[1]), 'datas': answer[0], 'type':'binary'})
            vals['value_file'] = int(attachment.id if attachment else False)
            vals['filename'] = attachment.name if attachment else False
        else:
            if isinstance(answer, str):
                vals['value_text_box'] = answer
            else:
                vals['value_char_box'] = str(answer)
        return vals
