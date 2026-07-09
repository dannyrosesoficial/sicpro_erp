# -*- coding: utf-8 -*-

from odoo import fields, models


class SurveyQuestionAnswer(models.Model):
    """Inherit question answer model to add new answer type and model fieldHeredar el modelo de pregunta y respuesta
    para agregar un nuevo tipo de respuesta y campo de modelo"""
    _inherit = 'survey.question.answer'

    answer_type = fields.Selection(
        [('text_box', 'Cuadro de texto de varias líneas'), ('char_box', 'Cuadro de texto de una sola línea'),
         ('numerical_box', 'Valor numérico'), ('date', 'Fecha'), ('datetime', 'Fecha y hora'), ('time', 'Tiempo'),
         ('email', 'Correo electrónico'), ('password', 'Contraseña'), ('range', 'Rango'), ('month', 'Mes'),
         ('url', 'URL'), ('week', 'Semana'), ('color', 'Color'), ('many2one', 'Many2one')], help="Tipo de respuesta",
        string='Tipo de respuesta', readonly=False, store=True)
    model_id = fields.Many2one('ir.model', string='Model', domain=[('transient', '=', False)],
                               help="Seleccione el modelo para obtener sus valores en la encuesta.")
