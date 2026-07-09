# -*- coding: utf-8 -*-


from odoo import fields, models


class TransporteHistorial(models.Model):
    _name = "sicpro.app.transporte.historial"
    _description = "Historial del transporte"
    _order = "create_date desc, date_start desc"

    vehicle_id = fields.Many2one('sicpro.app.transporte.general',
                                 string="Vehículo", required=True)
    driver_id = fields.Many2one('sicpro.app.trabajadores.general',
                                string="Trabajador", required=True)
    date_start = fields.Date(string="Fecha de inicio")
    date_end = fields.Date(string="Fecha fin")
