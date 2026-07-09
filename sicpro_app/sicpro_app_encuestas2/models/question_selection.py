# -*- coding: utf-8 -*-
from odoo import fields, models
class QuestionSelection(models.Model):
    _name = 'question.selection'
    _description = 'Preguntas de selección'
    name = fields.Char(string='Name', help='Valor de selección.')
    question_id = fields.Many2one('survey.question', string='Pregunta')
