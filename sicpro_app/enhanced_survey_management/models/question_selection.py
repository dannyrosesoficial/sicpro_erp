# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import fields, models


class QuestionSelection(models.Model):
    _name = 'question.selection'
    _description = 'Opciones de Selección Personalizada'
    _order = 'sequence, id' # Esto permite que se guarden en orden

    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    name = fields.Char(string='Nombre', required=True, help="Valor de la opción de selección.")
    question_id = fields.Many2one('survey.question', string="Pregunta", ondelete='cascade',
                                  help="Relación con la pregunta de la encuesta.")