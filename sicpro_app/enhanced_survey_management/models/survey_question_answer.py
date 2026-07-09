# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import fields, models


class SurveyQuestionAnswer(models.Model):
    _inherit = 'survey.question.answer'

    answer_type = fields.Selection([('text_box', 'Caja de texto múltiple'), ('char_box', 'Línea de texto única'),
        ('numerical_box', 'Valor numérico'), ('time', 'Hora'), ('email', 'Email'), ('password', 'Contraseña'),
        ('range', 'Rango'), ('month', 'Mes'), ('url', 'URL'), ('week', 'Semana'), ('color', 'Color'),
        ('many2one', 'Relación Many2one')], string='Tipo de Respuesta', default='char_box')

    model_id = fields.Many2one('ir.model', string='Modelo', domain=[('transient', '=', False)],
                               help="Modelo para obtener valores en la encuesta.")