# -*- coding: utf-8 -*-

from odoo import fields, models


class QuestionSelection(models.Model):
    """Modelo para almacenar opciones para pregunta de tipo selección."""
    _name = 'question.selection'
    _description = 'Preguntas de selección'

    name = fields.Char(string='Name', help="Valor de selección.")
    question_id = fields.Many2one('survey.question', string="Pregunta",
                                  help="Campo para almacenar la identificación de la pregunta en el tipo de selección.")
