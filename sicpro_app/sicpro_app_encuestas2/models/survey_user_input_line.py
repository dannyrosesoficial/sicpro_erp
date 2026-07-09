# -*- coding: utf-8 -*-
import json
from datetime import datetime
from odoo import api, fields, models, _

class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    answer_type = fields.Selection(selection_add=[('url','URL'),('many2one','Many2one'),('many2many','Many2many'),('week','Semana'),('time','Tiempo'),('color','Color'),('email','Correo electrónico'),('month','Mes'),('name','Nombre'),('matrix','Matriz'),('address','Dirección'),('selection','selección'),('password','Contraseña'),('file','Archivo'),('qr','Código QR'),('barcode','Código de barras')])
    value_url = fields.Char(string='URL')
    value_email = fields.Char(string='Email')
    value_week = fields.Char(string='Week')
    value_color = fields.Char(string='Color')
    value_many2one = fields.Char(string='Many2one')
    value_many2one_option = fields.Char(string='Many2one option')
    value_many2many = fields.Text(string='Many2many values')
    value_time = fields.Char(string='Time (HH:MM)')
    value_matrix = fields.Text(string='Matrix values')
    value_selection = fields.Char(string='Selection value')
    value_password = fields.Char(string='Password value')
    value_range = fields.Char(string='Range value')
    value_file = fields.Many2one('ir.attachment', string='File')
    filename = fields.Char(string='Filename')
    file_data = fields.Binary(related='value_file.datas', string='File data')
    value_month = fields.Char(string='Month value')
    value_address = fields.Text(string='Address JSON')
    value_name = fields.Text(string='Name JSON')
    value_qr = fields.Char(string='QR value')
    value_barcode = fields.Char(string='Barcode value')

    def get_value_time(self):
        if self.value_time:
            s = str(self.value_time).strip()
            s = s.replace('.', ':')
            try:
                dt = datetime.strptime(s, '%H:%M')
                return dt.strftime('%H:%M')
            except Exception:
                return s
        return None

    def get_value_address(self, field):
        if not self.value_address:
            return ''
        try:
            data = json.loads(self.value_address)
            qid = str(self.question_id.id)
            return data.get(f'{qid}-{field}', '') if isinstance(data, dict) else ''
        except Exception:
            return ''

    def get_value_matrix(self, item):
        if not self.value_matrix:
            return None
        try:
            data = json.loads(self.value_matrix)
            qid = str(self.question_id.id)
            return data.get(f'{item}-{qid}', None)
        except Exception:
            return None

    def get_value_name(self, field):
        if not self.value_name:
            return ''
        try:
            data = json.loads(self.value_name)
            qid = str(self.question_id.id)
            return data.get(f'{qid}-{field}', '') if isinstance(data, dict) else ''
        except Exception:
            return ''

    @api.depends('answer_type')
    def _compute_display_name(self):
        for line in self:
            mapping = {
                'char_box': line.value_char_box,
                'text_box': (line.value_text_box[:50] + '...') if line.value_text_box else None,
                'numerical_box': line.value_numerical_box,
                'time': line.value_time,
                'month': line.value_month,
                'address': line.value_address,
                'name': line.value_name,
                'url': line.value_url,
                'many2one': line.value_many2one_option,
                'many2many': line.value_many2many,
                'week': line.value_week,
                'email': line.value_email,
                'range': line.value_range,
                'matrix': line.value_matrix,
                'password': line.value_password,
                'color': line.value_color,
                'selection': line.value_selection,
                'barcode': line.value_barcode,
                'qr': line.value_qr,
                'file': line.filename,
                'date': fields.Date.to_string(line.value_date) if line.value_date else None,
                'datetime': fields.Datetime.to_string(line.value_datetime) if line.value_datetime else None,
            }
            if line.answer_type == 'suggestion':
                line.display_name = (f"{line.suggested_answer_id.value}: {line.matrix_row_id.value}" if line.matrix_row_id else line.suggested_answer_id.value)
            else:
                line.display_name = mapping.get(line.answer_type, None) or _('Skipped')
