# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SicproDBAuditLog(models.Model):
    _name = 'sicpro.app.db.audit.log'
    _description = 'Registro de Auditoría de Cambios Crudos'
    _order = 'change_date desc'

    name = fields.Char(string="Operación", readonly=True)
    user_id = fields.Many2one('res.users', string="Usuario", readonly=True, default=lambda self: self.env.user)
    model_name = fields.Char(string="Tabla/Modelo", readonly=True)
    res_id = fields.Integer(string="ID del Registro", readonly=True)
    field_name = fields.Char(string="Campo Modificado", readonly=True)
    old_value = fields.Text(string="Valor Anterior", readonly=True)
    new_value = fields.Text(string="Valor Nuevo", readonly=True)
    change_date = fields.Datetime(string="Fecha/Hora", default=fields.Datetime.now, readonly=True)

    @api.model
    def log_change(self, model, res_id, field, old, new):
        """Método auxiliar para crear registros de log"""
        self.create({
            'name': f"Modificación en {model} (ID: {res_id})",
            'model_name': model,
            'res_id': res_id,
            'field_name': field,
            'old_value': str(old),
            'new_value': str(new),
        })
