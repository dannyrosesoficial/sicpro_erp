# -*- coding: utf-8 -*-

from odoo import fields, models


class ContratosUnidades(models.Model):
    _name = 'sicpro.app.contratos.unidades'
    _description = 'Unidades de los contratos'
    _order = "id asc"

    name = fields.Char('Unidad', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "La unidad del contrato existe!"), ]




