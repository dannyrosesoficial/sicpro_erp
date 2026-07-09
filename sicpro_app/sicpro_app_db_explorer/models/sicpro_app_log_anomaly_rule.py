# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields

class SicproLogAnomalyRule(models.Model):
    _name = 'sicpro.log.anomaly.rule'
    _description = 'Reglas de Detección de Anomalías'

    name = fields.Char(string="Nombre de la Regla", required=True)
    keyword = fields.Char(string="Palabra Clave o Patrón", required=True)
    trigger_alert = fields.Boolean(string="Enviar Correo", default=True)
    severity_id = fields.Many2one('sicpro.log.severity', string="Severidad Asignada")
