# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import json
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    """Herencia para hacer el input de usuario compatible con preguntas personalizadas."""
    _inherit = "survey.user_input"

    def _save_lines(self, question, answer, comment=None, **kwargs):
        """
        Función para guardar respuestas personalizadas.
        En Odoo 19, 'overwrite_existing' se maneja vía **kwargs.
        """
        self.ensure_one()

        # Tipos de pregunta de SICPRO
        sicpro_types = ['password', 'range', 'time', 'url', 'email', 'many2many', 'file', 'many2one', 'week', 'color',
            'month', 'address', 'name', 'selection', 'qr', 'barcode', 'signature']

        # 1. Caso Matriz Personalizada
        if question.question_type == 'matrix' and question.matrix_subtype == 'custom':
            old_answers = self.user_input_line_ids.filtered(lambda l: l.question_id == question)
            return self._save_line_matrix(question, old_answers, answer, comment)

        # 2. Caso Tipos SICPRO Simples
        if question.question_type in sicpro_types:
            # En v19 eliminamos explícitamente para evitar error 'skipped vs answered'
            self.user_input_line_ids.filtered(lambda l: l.question_id == question).unlink()

            if question.question_type == 'selection':
                return self._save_line_selection_answer(question, answer)

            vals = self._get_line_answer_values(question, answer, question.question_type)
            if comment:
                vals['value_char_box'] = comment
            return self.env['survey.user_input.line'].create(vals)

        # 3. Caso Nativo de Odoo
        return super(SurveyUserInput, self)._save_lines(question, answer, comment, **kwargs)

    def _get_line_answer_values(self, question, answer, answer_type):
        """
        Método original de v17 para mapear valores a campos técnicos.
        Adaptado para asegurar consistencia de tipos en Odoo 19.
        """
        is_empty = not answer or (isinstance(answer, str) and not answer.strip())

        vals = {'user_input_id': self.id, 'question_id': question.id, 'survey_id': self.survey_id.id,
            'skipped': is_empty, 'answer_type': answer_type if not is_empty else False, }

        if is_empty:
            return vals

        # Lógica de asignación de campos según el tipo de respuesta
        if answer_type == 'time':
            vals['value_time'] = float(str(answer).replace(":", "."))
        elif answer_type in ['url', 'password', 'email', 'range', 'week', 'color', 'month', 'barcode', 'qr']:
            vals[f'value_{answer_type}'] = answer
        elif answer_type == 'many2one':
            if isinstance(answer, (list, tuple)) and len(answer) >= 2:
                vals['value_many2one'] = str(answer[0])
                vals['value_many2one_option'] = str(answer[1])
        elif answer_type == 'many2many':
            vals['value_many2many'] = str(answer)
        elif answer_type in ['address', 'name', 'signature', 'matrix']:
            # Aseguramos que se guarde como string (JSON) si viene como dict/list
            vals[f'value_{answer_type}'] = json.dumps(answer) if not isinstance(answer, (str, bytes)) else answer
        elif answer_type == 'file':
            attachment = self.env['ir.attachment'].sudo().create(
                {'name': str(answer[1]) if len(answer) > 1 else 'upload_file', 'datas': answer[0],
                    'res_model': 'survey.user_input.line', })
            vals.update({'value_file': attachment.id, 'filename': attachment.name})
        elif answer_type == 'selection':
            vals['value_selection'] = answer

        return vals

    def _save_line_matrix(self, question, old_answers, answers, comment):
        """Método original para guardar matrices con subtipo custom."""
        if question.matrix_subtype == 'custom':
            # Eliminamos las anteriores antes de crear la nueva para cumplir constrains de v19
            old_answers.sudo().unlink()
            vals = self._get_line_answer_values(question, answers, 'matrix')
            if comment:
                vals['value_char_box'] = comment
            return self.env['survey.user_input.line'].create(vals)

        # Si no es custom, usamos el método estándar de Odoo
        return super(SurveyUserInput, self)._save_line_matrix(question, old_answers, answers, comment)

    def _save_line_selection_answer(self, question, answer):
        """Método original para guardar respuestas de tipo selección."""
        vals = self._get_line_answer_values(question, answer, question.question_type)
        return self.env['survey.user_input.line'].create(vals)