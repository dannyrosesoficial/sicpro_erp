# -*- coding: utf-8 -*-

import json
import textwrap
from datetime import datetime

from odoo import api, fields, models, _


class SurveyUserInputLine(models.Model):
    """Línea de entrada de usuario heredada para agregar tipos de respuestas personalizados """
    _inherit = 'survey.user_input.line'

    answer_type = fields.Selection(
        selection_add=[('url', 'URL'), ('many2one', 'Many2one'), ('week', 'Semana'),
                       ('time', 'Tiempo'), ('color', 'Color'), ('email', 'Correo electrónico'), ('month', 'Mes'),
                       ('name', 'Nombre'), ('matrix', 'Matriz'), ('address', 'Dirección'), ('selection', 'selección'),
                       ('password', 'Contraseña'), ('email', 'Correo electrónico'), ('range', 'Rango'),
                       ('file', 'Archivo'), ('qr', 'Código QR'), ('barcode', 'Código de barras')],
        help="Tipos de respuesta personalizados")
    value_url = fields.Char(string='URL de usuario', help='Tipo de pregunta de respuesta: URL')
    value_email = fields.Char(string='Correo electrónico del usuario',
                              help="Tipo de pregunta de respuesta: Correo electrónico")
    value_week = fields.Char(string='Semana del usuario', help="Tipo de pregunta de respuesta: Semana")
    value_color = fields.Char(string='Color de usuario', help="Tipo de pregunta de respuesta: Color")
    value_many2one = fields.Char(string='Encuesta Many2one', help="Tipo de pregunta de respuesta: Many2one")
    value_many2one_option = fields.Char(string='Many2one seleccionado',
                                        help="Tipo de pregunta de respuesta: Seleccionada")
    value_time = fields.Float(string='Valor de tiempo', help="Tipo de pregunta de respuesta: Hora")
    value_matrix = fields.Text(string='Valores de matriz personalizados',
                               help="Tipo de pregunta de respuesta: Matriz personalizada")
    value_selection = fields.Char(string='Selección de usuario', help="Tipo de pregunta de respuesta: Selección")
    value_password = fields.Char(string='Valor de contraseña', help="Tipo de pregunta de respuesta: Contraseña")
    value_range = fields.Char(string='Valor de rango', help="Tipo de pregunta de respuesta:Rango")
    value_file = fields.Many2one('ir.attachment', string='Archivo de encuesta',
                                 help="Tipo de pregunta de respuesta: Adjunto")
    filename = fields.Char(string='Archivo', help="Nombre del archivo adjunto")
    file_data = fields.Binary(string='Datos de archivo', help="Datos del archivo adjunto", related="value_file.datas")
    value_month = fields.Char(string='Valor del mes', help="Tipo de pregunta de respuesta: Mes")
    value_address = fields.Text(string='Valor de dirección', help="Tipo de pregunta de respuesta: Dirección")
    value_name = fields.Text(string='Valores de nombre', help="Tipo de pregunta de respuesta: Nombre completo")
    value_qr = fields.Char(string='Valores QR', help="Answer question type : Código qr")
    value_barcode = fields.Char(string='Valores de código de barras',
                                help="Tipo de pregunta de respuesta: Código de barras")
    id_count = fields.Integer(string='Id_count', required=False)
    value_comment = fields.Text('Comment')

    def get_value_time(self):
        """Función para devolver respuesta para el tiempo de tipo pregunta. """
        if self.value_time:
            return datetime.strptime(str(self.value_time).replace('.', ':'), "%H:%M").strftime("%H:%M")
        return None

    def get_value_address(self, field):
        """Función para devolver respuesta para dirección de tipo de pregunta"""
        data = json.loads(self.value_address)
        if data:
            question_id = self.question_id.id
            return data[f'{question_id}-{field}']
        return ''

    def get_value_matrix(self, item):
        """Función para devolver respuesta para matriz personalizada"""
        data = json.loads(self.value_matrix)
        if data:
            question_id = self.question_id.id
            return data[f'{item}-{question_id}']
        return None

    def get_value_name(self, field):
        """Función para devolver respuesta para el nombre completo"""
        data = json.loads(self.value_name)
        if data:
            question_id = self.question_id.id
            return data[f'{question_id}-{field}']
        return ''

    @api.depends('answer_type')
    def _compute_display_name(self):
        """Anule la función de cálculo para agregar una visualización de respuesta personalizada"""
        for line in self:
            # Mapeo de tipo_respuesta al valor correspondiente
            answer_type_mapping = {'char_box': line.value_char_box,
                                   'text_box': textwrap.shorten(line.value_text_box, width=50,
                                                                placeholder=" [...]") if line.value_text_box else None,
                                   'numerical_box': line.value_numerical_box, 'time': line.value_time,
                                   'month': line.value_month, 'address': line.value_address, 'name': line.value_name,
                                   'url': line.value_url, 'many2one': line.value_many2one_option,
                                   'week': line.value_week,
                                   'email': line.value_email, 'range': line.value_range, 'matrix': line.value_matrix,
                                   'password': line.value_password,
                                   'color': line.value_color, 'selection': line.value_selection,
                                   'barcode': line.value_barcode, 'qr': line.value_qr, 'file': line.filename,
                                   'date': fields.Date.to_string(line.value_date) if line.value_date else None,
                                   'datetime': fields.Datetime.to_string(
                                       line.value_datetime) if line.value_datetime else None, }

            # Caso especial para 'sugerencia'
            if line.answer_type == 'suggestion':
                line.display_name = (
                    f"{line.suggested_answer_id.value}: {line.matrix_row_id.value}" if line.matrix_row_id else line.suggested_answer_id.value)
            else:
                # Obtener valor del mapeo o por defecto 'Omitido'
                line.display_name = answer_type_mapping.get(line.answer_type, None) or _('Skipped')
