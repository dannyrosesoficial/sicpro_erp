# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields, api
import os

class LogSource(models.Model):
    _name = 'sicpro.log.source'
    _description = 'Fuentes de Logs (Archivos, Docker, BD)'

    name = fields.Char(string="Nombre de la Fuente", required=True)
    file_path = fields.Char(string="Ruta Absoluta / Socket", required=True)
    source_type = fields.Selection([
        ('file', 'Archivo Local'),
        ('docker', 'Contenedor Docker'),
        ('db', 'Base de Datos')
    ], string="Tipo de Fuente", default='file', required=True)
    active = fields.Boolean(default=True, index=True)
    tag_ids = fields.Many2many('sicpro.log.tag', string="Etiquetas Asociadas")
    last_read_position = fields.Integer(string="Última Posición Leída (Bytes)", default=0)

    @api.model
    def _cron_read_all_sources(self):
        # Lógica base para lectura cronificada
        sources = self.search([('active', '=', True), ('source_type', '=', 'file')])
        for source in sources:
            if os.path.exists(source.file_path):
                # Placeholder para la lógica de lectura parcial de OS usando seek
                pass

class LogSeverity(models.Model):
    _name = 'sicpro.log.severity'
    _description = 'Mapeo de Severidad'

    name = fields.Char(string="Nivel", required=True)
    code = fields.Char(string="Código", required=True)
    color = fields.Integer(string="Color (UI)")
    regex_pattern = fields.Char(string="Patrón Regex", required=True, help="Patrón para identificar este nivel en texto.")

class LogAnomalyRule(models.Model):
    _name = 'sicpro.log.anomaly.rule'
    _description = 'Reglas de Detección de Anomalías'

    name = fields.Char(string="Nombre de la Regla", required=True)
    keyword = fields.Char(string="Palabra Clave o Patrón", required=True)
    trigger_alert = fields.Boolean(string="Enviar Correo", default=True)
    severity_id = fields.Many2one('sicpro.log.severity', string="Severidad Asignada")

class LogTag(models.Model):
    _name = 'sicpro.log.tag'
    _description = 'Etiquetas de Log'

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")
