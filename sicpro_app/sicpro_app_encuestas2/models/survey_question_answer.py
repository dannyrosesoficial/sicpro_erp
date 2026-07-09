# -*- coding: utf-8 -*-
from odoo import fields, models
class SurveyQuestionAnswer(models.Model):
    _inherit = 'survey.question.answer'
    answer_type = fields.Selection(selection_add=[('time','Tiempo'),('email','Correo'),('password','Contraseña'),('url','URL'),('month','Mes'),('week','Semana'),('color','Color'),('many2one','Many2one')])
    model_id = fields.Many2one('ir.model', string='Model', domain=[('transient','=',False)])
